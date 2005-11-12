import widgets
from widgets.driver_ezt import Template as ezt
from pyPgSQL import PgSQL


# location of these pages on server
ROOT = "/"


### At the moment, it's convenient to write these templates in python strings.
### Should probably push them out to files if the site grows
class Outline(widgets.TemplateBlock):
  template = ezt(
"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
<title>[title]</title>
<style>
<!--
  h2 { text-align: center; }
  body { font-family: Modern, Trebuchet MS, Arial, Helvetica, sans-serif; }
  .notugly { font-family: Trebuchet MS, Arial, Helvetica, sans-serif; }
-->
</style>
</head>
<body bgcolor="#E0E0E0">
[body]
</body>
</html>""")


class NavBar(widgets.TemplateBlock):
  root = ROOT
  template = ezt(
"""<script>
<!--

function setCaption(c)
{
  if (document.getElementById)
  {
    var e = document.getElementById("caption");
    if (!e.defaultText) e.defaultText = e.innerHTML;
    e.innerHTML = c;
    e.hover = true;
  }
}

function revertCaption()
{
  if (document.getElementById)
  {
    var e = document.getElementById("caption");
    e.hover = false;
    window.setTimeout("reallyRevertCaption()",50);
  }
}

function reallyRevertCaption()
{
  if (document.getElementById)
  {
    var e = document.getElementById("caption");
    if (!e.hover) e.innerHTML = e.defaultText;
  }
}

// -->
</script>
<p align=center>

[for links]
[define mousecap][if-any links.href]<i>[links.caption]</i>[else][links.caption][end][end]
[define mousey] onmouseover="setCaption('[mousecap]')" onmouseout="revertCaption()"[end]
[define img]<img src="[root][if-any links.href][links.img][else][links.imgglow][end]" width="[links.width]" height="[links.height]" alt="[links.caption]"[mousey] border=0>[end]
[if-any links.href]<a href="[root][links.href]"[mousey]>[img]</a>[else][img][end]
[end]
</p>

<h2 id=caption>[caption]</h2>""")

  def __init__(self, page):
    self.caption = page.title
    self.links = [ kw(page=HomePage, width=134, height=260,
                      img="media/student.gif",
                      imgglow="media/student_glow.gif"),
                   kw(page=ResumePage, width=115, height=249,
                      img="media/lawyer.gif",
                      imgglow="media/lawyer_glow.gif"),
                   kw(page=ProjectPage, width=171, height=238,
                      img="media/kneeling.gif",
                      imgglow="media/kneeling_glow.gif"),
                   kw(page=LinksPage, width=107, height=103,
                      img="media/bird.gif",
                      imgglow="media/bird_glow.gif") ]
    for link in self.links:
      if isinstance(page, link.page):
        link.href = None
      else:
        link.href = link.page.url
      link.caption = link.page.title


class BasePage(widgets.TemplateBlock):
  """Base class for all the site's pages, sets up outline and navbar"""
  def __init__(self):
    self.navbar = NavBar(self).var()

  def write(self, req):
    Outline(title=self.title, body=self.var()).write(req)


class HomePage(BasePage):
  title = "Home"
  url = "index.py"
  template = ezt(
"""[navbar]
<div class=notugly>
<p>Hi, I'm Russ Yanofsky, a computer science major at Columbia University's School of Engineering. This is my homepage, built to hold my resume, some links, and the source code for some programming projects I've worked on. </p>
</div>""")


class ResumePage(BasePage):
  title = "Resume"
  url = "resume.py"
  template = ezt(
"""[navbar]
<div class=notugly>
<p>Now in assorted formats:</p>
<ul>
  <li>Microsoft Word (<a href="resume.doc">resume.doc</a>, 31,744 bytes)</li>
  <li>HTML (<a href="resume.htm">resume.htm</a>, 19,070 bytes)</li>
  <li>PDF (<a href="resume.pdf">resume.pdf</a>, 48,559 bytes)</li>
  <li>Postscript (<a href="resume.ps">resume.ps</a>, 109,844 bytes)</li>
</ul>
</div>""")


class ProjectPage(BasePage):
  url = "projects.py"
  title = "Projects"
  template = ezt(
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
    <option>Size(ascending)</option>
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

  def __init__(self):
    BasePage.__init__(self)
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
          self.languages.append(kw(id=language_id, name=name))

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
          project = kw()
          (project.id, project.name, project.lines, project.cvs,
           project.description, project.dates, project.langs) = row
          self.projects.append(project)

      finally:
        cursor.close()
    finally:
      conn.close()


class LinksPage(BasePage):
  url = "links.py"
  title = "Links"
  template = ezt(
"""[navbar]
<div class=notugly>

<h3>Reading</h3>

<p>
<a href="http://www.theatlantic.com/">Atlantic Monthly</a>,
<a href="http://www.wsj.com/">Wall Street Journal</a>,
<a href="http://www.sciam.com/">Scientific American</a>,
<a href="http://www.economist.com/">Economist</a>,
<a href="http://www.nytimes.com/">New York Times</a>,
<a href="http://www.washingtonpost.com/">Washington Post</a>,
<a href="http://www.csmonitor.com">Christian Science Monitor</a>,
<a href="http://slashdot.org/">Slashdot</a> (<a href="http://www.cs.washington.edu/homes/klee/misc/slashdot.html">or not</a>),
<a href="http://memepool.com/">Memepool</a>,
<a href="http://www.mcsweeneys.net/">McSweeneys</a>,
<a href="http://slate.msn.com/">Slate</a>
</p>

<h3>Useful Sites</h3>

<p>
<a href="http://www.google.com/">Google</a>,
<a href="http://groups.google.com/">Google Groups</a>,
<a href="http://www.google.com/univ/columbia">Google Columbia</a>,
<a href="http://www.dictionary.com/">Dictionary</a>,
<a href="http://dictionary.oed.com/entrance.dtl">OED</a>,
<a href="http://www.columbia.edu/~rey4/classes.html">Classes</a>,
<a href="http://astalavista.box.sk/">astalavista</a> (turn off popups for this),
<a href="http://msdn.microsoft.com/workshop/author/dhtml/reference/objects.asp">DHTML Reference</a>
</p>

<h3>Pages and Sites on this Machine</h3>
<ul>
  <li><a href="http://cvs.russ.hn.org/viewcvs.asp/">cvs.russ.hn.org</a> - CVS Web</li>
  <li><a href="/cvcomputer/">/cvcomputer/</a> - Club I founded in high school</li>
  <li><a href="/jica/">/jica/</a> - java citrix client</li>
  <li><a href="/twofish/twofish.html">/twofish/</a> - javascript encryption utility (MD5, twofish)</li>
  <li><a href="/easycrt/">/easycrt/</a> - EasyCRT pascal graphics library</li>
  <li><a href="/cs1007/">/cs1007/</a>, <a href="/cs3156/">/cs3156/</a> - Web pages for classes</li>
  <li><a href="/reference/">/reference/</a> - cached copies of slow pages</li>
</ul>

<h3>Miscellany</h3>
<ul>
  <li><a href="http://www.godecookery.com/clipart/clart.htm">Medieval Woodcuts Clipart Collection</a> - site's graphics come from here</li>
  <li><a href="http://oracle.seas.columbia.edu/wces/">WCES</a></li>
</ul>
</div>""")


class kw:
  def __init__(self, **kw):
    vars(self).update(kw)


# ========================================================================== #
# Mod_Python handler
# ========================================================================== #


from mod_python import apache
from widgets import driver_mod_python


_pages = { ROOT: HomePage }
for page in (HomePage, ResumePage, ProjectPage, LinksPage):
  _pages[ROOT + page.url] = page


def handler(req):
  try:
    page = _pages[req.uri]
  except KeyError:
    raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

  req.content_type = 'text/html'
  page().write(driver_mod_python.Request(req))

  return apache.OK
