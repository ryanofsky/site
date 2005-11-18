import widgets
from widgets.driver_ezt import Template as ezt


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
[define href][is caption links.caption][else]yes[end][end]
[define mousey] onmouseover="setCaption('[if-any href]<i>[links.caption]</i>[else][links.caption][end]')" onmouseout="revertCaption()"[end]
[define img]<img src="[root][if-any href][links.img][else][links.imgglow][end]" width="[links.width]" height="[links.height]" alt="[links.caption]"[mousey] border=0>[end]
[if-any href]<a href="[root][links.href]"[mousey]>[img]</a>[else][img][end]
[end]
</p>

<h2 id=caption>[caption]</h2>""")

  def __init__(self, caption):
    self.caption = caption
    self.links = [ kw(caption="Home", href="index.py",
                      img="media/student.gif",
                      imgglow="media/student_glow.gif",
                      width=134, height=260),
                   kw(caption="Resume", href="resume.py",
                      img="media/lawyer.gif",
                      imgglow="media/lawyer_glow.gif",
                      width=115, height=249),
                   kw(caption="Projects", href="projects.py",
                      img="media/kneeling.gif",
                      imgglow="media/kneeling_glow.gif",
                      width=171, height=238),
                   kw(caption="Links", href="links.py",
                      img="media/bird.gif",
                      imgglow="media/bird_glow.gif",
                      width=107, height=103) ]


class BasePage(widgets.TemplateBlock):
  """Base class for all the site's pages, sets up outline and navbar"""
  def __init__(self):
    self.navbar = NavBar(self.title).var()

  def write(self, req):
    Outline(title=self.title, body=self.var()).write(req)


class kw:
  def __init__(self, **kw):
    vars(self).update(kw)

# ========================================================================== #
# CGI handler
# ========================================================================== #

def handle_cgi(page):
  from widgets import driver_cgi
  req = driver_cgi.Request()
  req.write('Content-Type: text/html\r\n\r\n')
  page.write(req)

# ========================================================================== #
# Mod_Python handler
# ========================================================================== #

import os.path

def handler(req):
  global apache, driver_mod_python
  from mod_python import apache
  from widgets import driver_mod_python

  # based on publisher.py
  path, module_name =  os.path.split(req.filename)
  module_name, module_ext = os.path.splitext(module_name)
  try:
    module = apache.import_module(module_name, path=[path])
  except ImportError:
    raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

  req.content_type = 'text/html'
  module.Page().write(driver_mod_python.Request(req))

  return apache.OK
