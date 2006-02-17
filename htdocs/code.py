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
<form action="[form.url]" name="[form.name]">

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
</form>

<p>[num_projects] projects found</p>

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
</div>
[footer]""")

  sorts = (("datedown", "Date (descending)"),
           ("dateup", "Date (ascending)"),
           ("sizedown", "Size (descending)"),
           ("sizeup", "Size (ascending)"))

  def __init__(self, req):
    web.BasePage.__init__(self, req)

    self.form = widgets.Form(req, "code")

    bw = self.template.bind_write
    conn = connect(self.form)

    order = widgets.SelectBox(req, self.form, "order", widgets.READ_FORM)
    self.order = bw(order.write, self.sorts)

    langs = widgets.MSelectBox(req, self.form, "langs", widgets.READ_FORM)
    self.langs = bw(langs.write, get_langs(conn),
                    default="--- Any Language ---")

    self.num_projects = num_projects(conn, langs.selected)
    self.projects = get_projects(conn, langs.selected, order.selected, "", "")


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
        "limit": limit and "LIMIT %i" % int(limit) or "",
        "offset": offset and "OFFSET %i" % int(offset) or "" })

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
