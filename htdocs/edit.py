#!/usr/bin/env python

from pyPgSQL import PgSQL
import web
import widgets
from widgets import ezt


# ======================================================================
# Database Logic

class Table:
  def __init__(self, name, id_col, id_seq, cols):
    self.name = name
    if id_col:
      self.id_col = id_col
      self.id_readonly = False
    else:
      self.id_col = "oid"
      self.id_readonly = True
    self.id_seq = id_seq
    self.cols = cols

  def delete(self, cursor, id):
    self._query(cursor, "DELETE FROM %s WHERE %s = %%s"
                        % (self.name, self.id_col), id)

  def insert(self, cursor, vals):
    self._query(cursor, "INSERT INTO %s (%s) VALUES (%s)"
                        % (self.name,
                           ", ".join(self.cols),
                           ", ".join(("%s",) * len(self.cols))), vals)
    if self.id_seq:
      cursor.callproc("currval", self.id_seq)
      return cursor.fetchone()[0]

  def update(self, cursor, id, vals):
    if self.id_readonly:
      update_cols = self.cols
    else:
      update_cols = (self.id_col,) + self.cols

    self._query(cursor, "UPDATE %s SET %s WHERE %s = %%s"
                        % (self.name,
                           ", ".join(["%s = %%s" % col
                                      for col in update_cols]),
                           self.id_col), vals + [id])

  def select(self, cursor, id):
    self._query(cursor, "SELECT %s FROM %s WHERE %s = %%s"
                        % (", ".join(self.cols),
                           self.name,
                           self.id_col), id)
    return cursor.fetchone()

  def select_all(self, cursor):
    self._query(cursor, "SELECT %s, %s FROM %s ORDER BY %s"
                        % (self.id_col,
                           ", ".join(self.cols),
                           self.name,
                           self.id_col))
    while True:
      row = cursor.fetchone()
      if not row:
        break
      yield row

  def _query(self, cursor, sql, *args):
    try:
      cursor.execute(sql, *args)
    except PgSQL.DatabaseError, e:
      raise DbError(e, sql)

class DbError(Exception):
  def __init__(self, error, sql=None):
    self.error = error
    self.sql = sql

  def __str__(self):
    return str(self.error)

tables = {
  "projects": Table("projects", "project_id", "project_ids",
                    ("name", "lines", "cvsmodule", "startdate", "enddate",
                     "description")),
  "languages": Table("languages", "language_id", "language_ids", ("name",)),
  "project_languages": Table("project_languages", None, None,
                             ("project_id", "language_id"))
}

def connect(form):
  if not hasattr(form, "db"):
    try:
      form.db = PgSQL.connect("::projects:postgres:::")
    except PgSQL.DatabaseError, e:
      raise DbError(e)
  return form.db


# ======================================================================
# Web Logic

class Page(web.BasePage):
  DATE = "$Date$"
  title = "Table Editor"
  template = web.ezt(
"""
<form action="[form.url]" name="[form.name]">
[editor]
</form>
[footer]""")

  def __init__(self, req):
    web.BasePage.__init__(self, req)
    self.form = widgets.Form(req, "edit")
    editor = TableEditor(req, self.form, "table", widgets.READ_FORM)
    self.editor = self.template.bind_write(editor.write)

class TableEditor(widgets.ModalWidget):
  template = web.ezt(
r"""[message]
<div>Table [chooser "onchange=\"this.form.submit()\"" "poop"]
<input type="submit" value="Set">
</div>

<table border=1 bordercolor=black cellpadding=3 cellspacing=0>
  <thead>
    <tr>
      <td>[id_col]</td>
      [for cols]<td>[cols]</td>[end]
      <td>&nbsp;</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="[table_cols]" style="text-align:center">
        [insert "Insert New Row..."]
      </td>
    </tr>
    [for rows]
      <tr>
        [for rows.cols]<td>[rows.cols]</td>[end]
        <td>[rows.edit "Edit"] [rows.delete "Delete"]</td>
      </tr>
    [end]
  </tbody>
</table>""")

  EDIT = "edit"
  DELETE = "delete"

  def __init__(self, req, parent, id, flags):
    widgets.ModalWidget.__init__(self, req, parent, id, flags)

    # set members
    self.chooser = widgets.SelectBox(req, self, "chooser", flags)
    self.message = None
    if self.chooser.selected is None:
      self.table = tables.values()[0]
    else:
      self.table = tables[self.chooser.selected]

    # initialize mode, quit if there's an active child
    self.read_mode(req, flags)
    if self.init_children(req, flags):
      return

    # handle button clicks
    self.button = widgets.DataButton(req, self, "button", flags)
    command = self.parse_mode(self.button.clicked)
    if command:
      if command[0] == self.DELETE:
        # Delete button pressed
        error = None
        try:
          conn = connect(self.form)
          self.table.delete(conn.cursor(), command[1])
          conn.commit()
        except DbError, e:
          error = e
        self.message = Message(req, delete=True, row=command[1], error=error)

      elif command[0] == self.EDIT:
        # Edit button pressed
        self.mode = command
        self.init_children(req, flags | widgets.READ_DEFAULT)

  def init_children(self, req, flags):
    if self.mode is not None:
      if self.mode[0] == self.EDIT:
        row = None
        if len(self.mode) > 1:
          row = int(self.mode[1])

        self.editor = RowEditor(req, self, "row", flags, self.table, row)
        if self.editor.active:
          return True

        self.mode = None
        self.message = self.editor.message
        self.modal_children.remove(self.editor)
        del self.editor

    return False

  def write(self, req):
    # preserve mode, if there's an active child widget, show it and return
    self.write_mode(req)
    if self.write_children(req):
      self.chooser.write_hidden(req, widgets.WRITE_FORM)
      return

    # execute template
    bw = self.template.bind_write
    data = web.kw(message=self.message and bw(self.message.write),
                  chooser=bw(self.chooser.write, tables.keys()),
                  id_col=self.table.id_col,
                  cols=self.table.cols,
                  table_cols=len(self.table.cols) + 2,
                  insert=bw(self.button.write, self.mode_str((self.EDIT, ))),
                  rows=self.rows())

    self.template.execute(req, data)

  def rows(self):
    # generator for "rows" template variable
    cursor = connect(self.form).cursor()
    bw = self.template.bind_write
    for row in self.table.select_all(cursor):
      yield web.kw(cols=map(str, row),
                   edit=bw(self.button.write,
		           self.mode_str((self.EDIT, row[0]))),
                   delete=bw(self.button.write,
                             self.mode_str((self.DELETE, row[0]))))

class RowEditor(widgets.ModalWidget):
  """Row Editor Widget

  Public members

   message - message object"""

  template = web.ezt(
"""
[message]
<table>
  [if-any auto_field]
    <tr>
      <td>[auto_field]</td>
      <td><em>[if-any auto_val][auto_val][else]auto[end]</em></td>
    </tr>
  [end]
  [for fields]
    <tr>
      <td>[fields.name]</td>
      <td>[fields.control "50"]</td>
    </tr>
  [end]
</table>
[save "Save"] [cancel "Cancel"]""")

  def __init__(self, req, parent, id, flags, table, row):
    widgets.ModalWidget.__init__(self, req, parent, id, flags)
    self.table = table
    self.row = row
    self.message = None

    # Create text boxes for columns
    self.cols = []
    if row is not None and not self.table.id_readonly:
      self.cols.append(widgets.TextBox(req, self, self.table.id_col, flags))
    for col in self.table.cols:
      self.cols.append(widgets.TextBox(req, self, col, flags))

    # Save and cancel buttons
    self.save = widgets.SubmitButton(req, self, "save", flags)
    self.cancel = widgets.SubmitButton(req, self, "cancel", flags)

    # If widget being loaded for first time, load values from database
    if flags & widgets.READ_DEFAULT and self.row is not None:
      cursor = connect(self.form).cursor()
      vals = self.table.select(cursor, self.row)
      if vals:
        cols = iter(self.cols)
        if not self.table.id_readonly:
          cols.next().text = self.row
        for col, val in zip(cols, vals):
          col.text = val
      else:
        # Can't edit a row that no longer exists, exit and show message
        self.message = Message(req, not_found=True, row=self.row)
        self.active = False

    if self.save.clicked:
      # Save button pressed, either insert new row or update existing
      try:
        conn = connect(self.form)
        cursor = conn.cursor()
        if self.row is not None:
          self.table.update(cursor, self.row,
                            [col.text for col in self.cols])
          if self.table.id_readonly:
            saved_row = self.row
          else:
            saved_row = int(self.cols[0].text)
        else:
          saved_row = self.table.insert \
                      (cursor, [col.text for col in self.cols])
        conn.commit()
        self.active = False
        self.message = Message(req, save=True, row=saved_row)
      except DbError, e:
        self.message = Message(req, save=True, row=self.row, error=e)

    elif self.cancel.clicked:
      self.active = False

  def write(self, req):
    # template data
    bw = self.template.bind_write
    data = web.kw(message=self.message and bw(self.message.write),
                  auto_field=None,
                  auto_val=None,
                  fields=[],
                  save=bw(self.save.write),
                  cancel=bw(self.cancel.write))

    # if inserting a new row or editing read only, id is filled automatically
    cols = self.table.cols
    if self.row is None or self.table.id_readonly:
      data.auto_field = self.table.id_col
      data.auto_val = self.row
    else:
      cols = (self.table.id_col,) + cols

    # add normal fields
    for name, control in zip(cols, self.cols):
      data.fields.append(web.kw(name=name, control=bw(control.write)))

    self.template.execute(req, data)

class Message(widgets.TemplateWidget):
  template = web.ezt(
"""[if-any error]
  <div style="color: red">
    [if-any save]Error: Row [row] Not Saved[end]
    [if-any delete]Error: Row [row] Not Deleted[end]
  </div>
  <pre>[error]</pre>
  [if-any sql]
    <div style="color:red">Query String:</div>
    <pre>[sql]</pre>
  [end]
[else]
  <div><em>
    [if-any save]Row [row] Saved[end]
    [if-any delete]Row [row] Deleted[end]
    [if-any not_found]Row [row] No Longer Exists[end]
  </em></div>
[end]""")

  def __init__(self, req, save=False, delete=False, not_found=False,
               row=None, error=None):
    self.save = widgets.ezt.boolean(save)
    self.delete = widgets.ezt.boolean(delete)
    self.not_found = widgets.ezt.boolean(not_found)
    self.row = row
    self.error = error and str(error)
    self.sql = error and error.sql


if __name__ == "__main__":
  web.handle_cgi(Page)
