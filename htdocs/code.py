#!/usr/bin/env python
import cgitb; cgitb.enable()
import web
import widgets
from pyPgSQL import PgSQL


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Code"
  template = web.ezt(
r"""[navbar]
<div class=notugly>

<a name="query"></a>

<form action="[form.url]#query" name="[form.name]">

<table border=1 cellpadding=3>
<tr>
  <td>Order by [order "size=\"1\""]</td>
</tr>
<tr>
  <td>
    Filter by Language<br>
    [langs "size=\"5\""]
  </td>
</tr>
<tr>
  <td align=center>
    <input type=submit name=submit value=Submit>
   </td>
</tr>
</table>

<p>[pager "head"]</p>

</form>


[for projects]
<table border=1 bordercolor=black cellpadding=3 cellspacing=0>
<tr><td>Name:</td><td>[projects.name]</td></tr>
<tr><td>Size:</td><td>[if-any projects.lines][projects.lines] lines[else]?[end]</td></tr>
<tr><td>Dates:</td><td>[projects.dates]</td></tr>
<tr><td nowrap>CVS Repository:</td><td>[if-any projects.cvs]<a href="[root]viewvc.py/[projects.cvs]/">[projects.cvs]</a>[else]<i>none</i>[end]</td></tr>
<tr><td>Language(s):</td><td>[projects.langs]</td></tr>
<tr><td valign=top>Description:</td><td>[projects.description]</td></tr>
</table><br>
[end]

[pager]

</div>
[footer]""")

  sorts = (("datedown", "Date (descending)"),
           ("dateup", "Date (ascending)"),
           ("sizedown", "Size (descending)"),
           ("sizeup", "Size (ascending)"))

  def __init__(self, req):
    web.BasePage.__init__(self, req)
    self.form = widgets.Form(req, "code")
    self._order = widgets.SelectBox(req, self.form, "order",
                                    widgets.READ_FORM)
    self._langs = widgets.MSelectBox(req, self.form, "langs",
                                     widgets.READ_FORM)
    self._pager = Pager(req, self.form, "pager", widgets.READ_FORM)

  def write(self, req):
    # preserve order and lang values in pager links
    self._order.write_hidden(req, widgets.WRITE_URL)
    self._langs.write_hidden(req, widgets.WRITE_URL)

    # expose child widgets write methods as template variables
    bw = self.template.bind_write
    conn = connect(self.form)

    self.order = bw(self._order.write, self.sorts)
    self.langs = bw(self._langs.write, get_langs(conn),
                    default="--- Any Language ---")
    self.pager = bw(self._pager.write,
                    num_projects(conn, self._langs.selected))
    self.projects = get_projects(conn,
                                 self._langs.selected,
                                 self._order.selected,
                                 self._pager.limit,
                                 self._pager.offset)

    # write the template
    web.BasePage.write(self, req)

class Pager(widgets.FormWidget):
  # number of items per page
  default_limit = 10

  template = web.ezt("""
  <div style="float: left">
    [if-any pages]
      Showing [first] - [last] of [num_projects] matches.</a>
    [else]
      [num_projects] matches found.
    [end]
  </div>
  <div style="float: right">
  [if-any pages]
    [for pages]
      [if-any pages.url]<a href="[pages.url]#query">[end]
      [pages.first][is pages.first pages.last][else]-[pages.last][end][if-any pages.url]</a>[end] |
    [end]
    <a href="[all_url]#query">All</a> |
    [if-any prev_url]<a href="[prev_url]#query">Prev</a>[else]Prev[end] |
    [if-any next_url]<a href="[next_url]#query">Next</a>[else]Next[end]
  [else]
    [if-any all_url]<a href="[all_url]#query">Show Pages</a>[end]
  [end]
  </div>
  <div>&nbsp;</div>

  """)

  def __init__(self, req, parent, id, flags):
    widgets.FormWidget.__init__(self, req, parent, id, flags)
    self.offset = int(self.read_value(req, "offset", flags) or 0)
    self.limit = int(self.read_value(req, "limit", flags)
                     or self.default_limit)

  def write(self, req, num_projects, header=False):
    # footer looks stupid when there aren't a lot of matches
    if not header and (num_projects < 3 or self.limit == 0):
      return

    # preserve current limit when form is submitted
    if header:
      self.write_value(req, "limit", str(self.limit), widgets.WRITE_FORM)

    data = web.kw(num_projects=num_projects,
                  header=header,
                  first=None,
                  last=None,
                  pages=[],
                  prev_url=None,
                  next_url=None,
                  all_url=None)

    # if there's more than one page...
    if self.limit and (num_projects > self.limit or self.offset):
      data.first = min(self.offset+1, num_projects)
      data.last = min(self.offset+self.limit, num_projects)

      for offset in range(0, num_projects, self.limit):
        page = web.kw(first=offset + 1,
                      last=min(offset+self.limit, num_projects),
                      url=None)
        if offset != self.offset:
          page.url = self.form.get_url([(self.id("offset"), str(offset)),
                                        (self.id("limit"), str(self.limit))])
        data.pages.append(page)

      if self.offset > 0:
        data.prev_url = data.pages[(self.offset - 1) // self.limit].url

      if self.offset + self.limit < num_projects:
        n = self.offset // self.limit + 1
        data.next_url = str(data.pages[n].url)

      data.all_url = self.form.get_url([(self.id("limit"), "0")])

    # if there's more than one page but we're forcing all results...
    elif not self.limit and num_projects > self.default_limit:
      data.all_url = self.form.get_url([(self.id("limit"),
                                         str(self.default_limit))])

    self.template.execute(req, data)


########################
# #  Database Logic  # #

def connect(form):
  if not hasattr(form, "db"):
    form.db = PgSQL.connect("::code:postgres:::")
  return form.db

def get_langs(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT language_id, name FROM languages "
                 "ORDER BY language_id")
  while True:
    row = cursor.fetchone()
    if not row:
      break
    language_id, name = row
    yield str(language_id), name
  cursor.close()

def num_projects(conn, languages):
  cursor = conn.cursor()
  cursor.execute("SELECT COUNT(*) FROM projects AS p %s"
                 % (languages and where_uses_lang("p", languages) or ""))
  return cursor.fetchone()[0]

def get_projects(conn, languages, order, limit, offset):
  cursor = conn.cursor()

  orderby = {"datedown": "p.startdate DESC",
             "dateup":   "p.startdate",
             "sizedown": "p.lines DESC",
             "sizeup":   "p.lines"}[order or "datedown"]

  cursor.execute("""
    SELECT p.project_id, p.name, p.lines, p.cvsmodule, p.description,
      (CASE WHEN p.startdate IS NULL THEN '?'
       ELSE to_char(p.startdate,'MM/DD/YYYY') END) || ' - '
      || (CASE WHEN p.enddate IS NULL THEN '?'
          ELSE to_char(p.enddate,'MM/DD/YYYY') END) AS dates,
      comma(l.name) AS langs
    FROM projects AS p
    INNER JOIN project_languages AS pl USING (project_id)
    INNER JOIN languages AS l USING (language_id)
    %(where)s
    GROUP BY p.project_id, p.name, p.lines, p.cvsmodule, p.description,
      p.startdate, p.enddate
    ORDER BY %(orderby)s
    %(limit)s
    %(offset)s"""
    % { "where": languages and where_uses_lang("p", languages) or "",
        "orderby": orderby,
        "limit": limit and "LIMIT %i" % limit or "",
        "offset": offset and "OFFSET %i" % offset or "" })

  while True:
    row = cursor.fetchone()
    if not row:
      break
    project = web.kw()
    (project.id, project.name, project.lines, project.cvs,
     project.description, project.dates, project.langs) = row
    yield project

  cursor.close()

def where_uses_lang(projects_table, languages):
  langs = ",".join([str(int(language_id)) for language_id in languages])
  return ("WHERE EXISTS (SELECT * FROM project_languages AS ulpl "
                        "WHERE ulpl.project_id = %s.project_id "
                        "AND ulpl.language_id IN (%s))"
          % (projects_table, langs))


if __name__ == '__main__':
  web.handle_cgi(Page)
