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
    self.id_col = id_col
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
    self._query(cursor, "UPDATE %s SET %s WHERE %s = %%s"
                        % (self.name,
                           ", ".join(["%s = %%s" % col
                                      for col in (self.id_col,) + self.cols]),
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
  "project_languages": Table("project_languages", "oid", None,
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
  title = "Table Editor"
  template = web.ezt(
"""<div class=notugly>
<form action="[form.url]" name="[form.name]">
[editor.write]
</form>
</div>""")

  def __init__(self, req):
    web.BasePage.__init__(self, req)
    self.form = widgets.Form(req, "edit")
    self.editor = TableEditor(req, self.form, "table", widgets.READ_FORM,
                              tables["languages"])

class TableEditor(widgets.FormWidget):
  template = web.ezt(
"""[message]
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
        [if-any rows.edit_cols]
           <td>
             [if-any rows.edit_id][rows.edit_id][else]<em>auto</em>[end]
           </td>
          [for rows.edit_cols]<td>[rows.edit_cols]</td>[end]
          <td>[rows.save "Save"] [rows.cancel "Cancel"]</td>
        [else]
           [for rows.cols]<td>[rows.cols]</td>[end]
           <td>[rows.edit "Edit"] [rows.delete "Delete"]</td>
        [end]
       </tr>
     [end]
  </tbody>
</table>""")

  EDIT = 1
  DELETE = 2
  SAVE = 3
  CANCEL = 4

  def parse_state(self, state):
    if state == "save":
      return self.SAVE, None
    elif state == "cancel":
      return self.CANCEL, None
    elif state:
      row = state[1:]
      if state[0] == "d":
        return self.DELETE, int(row)
      elif state[0] == "e":
        if row:
          return self.EDIT, int(row)
        return self.EDIT, None
    return None, None

  def state_str(self, (command, row)):
    if command == self.DELETE:
      return "d%i" % row
    elif command == self.EDIT:
      if row is not None:
        return "e%i" % row
      else:
        return "e"
    elif command == self.SAVE:
      return "save"
    elif command == self.CANCEL:
      return "cancel"

  def __init__(self, req, parent, id, flags, table):
    widgets.FormWidget.__init__(self, req, parent, id, flags)
    self.table = table
    self.message = None

    self.state = self.parse_state(self.read_value(req, "state", flags))
    self.button = widgets.DataButton(req, self, "button", flags)

    command = self.parse_state(self.button.clicked)
    new_state = False
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
      self.state = command
      new_state = True

    if self.state[0] == self.EDIT:
      # Edit state
      edit_row = self.state[1]
      edit_flags = flags | (new_state and widgets.READ_DEFAULT)

      # Text box for id column, only created if editing existing row
      self.edit_id = None
      if edit_row is not None:
        self.edit_id = widgets.TextBox(req, self, table.id_col, edit_flags)

      # Text boxes for other columns
      self.edit_cols = []
      for col in self.table.cols:
        self.edit_cols.append(widgets.TextBox(req, self, col, edit_flags))

      # If fields being shown for first time, load values from database
      if new_state and edit_row is not None:
        cursor = connect(self.form).cursor()
        vals = self.table.select(cursor, edit_row)
        if vals:
          self.edit_id.text = edit_row
          for col, val in zip(self.edit_cols, vals):
            col.text = val
        else:
          # Show a message on attempt to edit a row that no longer exists
          self.message = Message(req, not_found=True, row=edit_row)
          self.state = None, None

      if command[0] == self.SAVE:
        # Save button pressed, either insert new row or update existing
        try:
          conn = connect(self.form)
          cursor = conn.cursor()
          if edit_row is not None:
            self.table.update(cursor, edit_row,
                              [self.edit_id.text]
                              + [col.text for col in self.edit_cols])
            saved_row = int(self.edit_id.text)
          else:
            saved_row = self.table.insert \
              (cursor, [col.text for col in self.edit_cols])
          conn.commit()
          self.state = None, None
          self.message = Message(req, save=True, row=saved_row)
        except DbError, e:
          self.message = Message(req, save=True, row=edit_row, error=e)

      elif command[0] == self.CANCEL:
        # Cancel button pressed, reset state
        self.state = None, None

  def write(self, req):
    # preserve state
    self.write_value(req, "state", self.state_str(self.state),
                     widgets.WRITE_FORM)

    # execute template
    data = web.kw(message=self.message and self.message.write or "",
                  id_col=self.table.id_col,
                  cols=self.table.cols,
                  table_cols=len(self.table.cols) + 2,
                  insert=None,
                  rows=self.rows())

    insert_state = self.EDIT, None
    if self.state != insert_state:
      data.insert = self.button.write_cb(self.state_str(insert_state))

    self.template.execute(req, data)

  def rows(self):
    # generator for "rows" template variable
    edit_row = None
    if self.state[0] == self.EDIT:
      edit_row = self.state[1]
      edit_ret = web.kw(edit_id=self.edit_id and self.edit_id.write,
                        edit_cols=[col.write for col in self.edit_cols],
                        save=self.button.write_cb
                              (self.state_str((self.SAVE, None))),
                        cancel=self.button.write_cb
                              (self.state_str((self.CANCEL, None))))

      if edit_row is None:
        yield edit_ret

    cursor = connect(self.form).cursor()
    for row in self.table.select_all(cursor):
      if row[0] == edit_row:
        yield edit_ret
      else:
        yield web.kw(cols=row,
                     edit_cols=None,
                     edit=self.button.write_cb
                            (self.state_str((self.EDIT, row[0]))),
                     delete=self.button.write_cb
                              (self.state_str((self.DELETE, row[0]))))

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
