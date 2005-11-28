#!/usr/bin/env python
import web
from pyPgSQL import PgSQL


class Page(web.BasePage):
  title = "Projects"
  template = web.ezt(
"""[navbar]
<div class=notugly>
<form>

<p>It's taking a lot longer than I thought it would to gather source files, statistics, and comments for these projects.  I'm going to add to the content here and revise gradually over the next few weeks, as time permits. So far I've added all of the projects that have online CVS repositories or preexisting web sites.</p>
<p><i>Note:</i> These controls don't actually do anything right now. When I get the opportunity, I'll replace them with ASP.NET Web Form elements, so I'll be able to add functionality and learn a new API at once.</p>

<table border=1 cellpadding=3>
<tr>
  <td>Order by
    <select size=1>
    <option>Date (descending)</option>
    <option>Size (descending)</option>
    <option>Date (ascending)</option>
    <option>Size (ascending)</option>
    </select>
  </td>
</tr>
<tr>
  <td>
    Filter by Language<br>
    <select size=5 multiple>
    [for languages]
      <option value="[languages.id]">[languages.name]</option>
    [end]
    </select>
  </td>
</tr>
<tr>
  <td align=center>
    <input type=submit name=submit value=Submit>
   </td>
</tr>
</table>
</form>

[for projects]
<table border=1 bordercolor=black cellpadding=3 cellspacing=0>
<tr><td>Name:</td><td>[projects.name]</td></tr>
<tr><td>Size:</td><td>[if-any projects.lines][projects.lines] lines[else]?[end]</td></tr>
<tr><td>Dates:</td><td>[projects.dates]</td></tr>
<tr><td nowrap>CVS Repository:</td><td>[if-any]<a href="http://russ.hn.org/viewvc/[projects.cvs]/">[projects.cvs]</a>[projects.cvs][else]<i>none</i>[end]</td></tr>
<tr><td>Language(s):</td><td>[projects.langs]</td></tr>
<tr><td valign=top>Description:</td><td>[projects.description]</td></tr>
</table><br>
[end]
</div>""")

  def __init__(self, req):
    web.BasePage.__init__(self, req)
    conn = PgSQL.connect("::projects:postgres:::")
    try:
      cursor = conn.cursor()
      try:
        cursor.execute("SELECT language_id, name FROM languages "
                       "ORDER BY language_id");
        self.languages = []
        while 1:
          row = cursor.fetchone()
          if not row:
            break
          language_id, name = row
          self.languages.append(web.kw(id=language_id, name=name))

        self.projects = []
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
          GROUP BY p.project_id, p.name, p.lines, p.cvsmodule, p.description,
            p.startdate, p.enddate
          ORDER BY p.startdate DESC""")

        while True:
          row = cursor.fetchone()
          if not row:
            break
          project = web.kw()
          (project.id, project.name, project.lines, project.cvs,
           project.description, project.dates, project.langs) = row
          self.projects.append(project)

      finally:
        cursor.close()
    finally:
      conn.close()


if __name__ == '__main__':
  web.handle_cgi(Page)
