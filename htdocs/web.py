import widgets
from widgets.driver_ezt import Template as ezt


# location of these pages on server
ROOT = "/"


### At the moment, it's convenient to write these templates in python strings.
### Should probably push them out to files if the site grows
class Outline(widgets.TemplateWidget):
  template = ezt(
"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
<title>[title]</title>
<style>
<!--
  h2 { text-align: center; }
  body { font-family: Modern, Trebuchet MS, Arial, Helvetica, sans-serif;
         text-align: center; }
  .notugly { font-family: Trebuchet MS, Arial, Helvetica, sans-serif;
             margin-left: auto; margin-right: auto; width: 600px;
	     text-align: left; }
-->
</style>
</head>
<body bgcolor="#E0E0E0">
[body]
</body>
</html>""")


class NavBar(widgets.TemplateWidget):
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

  def __init__(self, req, caption):
    self.caption = caption
    self.links = [ kw(caption="Home", href="index.py",
                      img="media/student.gif",
                      imgglow="media/student_glow.gif",
                      width=134, height=260),
                   kw(caption="Resume", href="resume.py",
                      img="media/lawyer.gif",
                      imgglow="media/lawyer_glow.gif",
                      width=115, height=249),
                   kw(caption="Code", href="code.py",
                      img="media/kneeling.gif",
                      imgglow="media/kneeling_glow.gif",
                      width=171, height=238),
                   kw(caption="Links", href="links.py",
                      img="media/bird.gif",
                      imgglow="media/bird_glow.gif",
                      width=107, height=103) ]


class BasePage(widgets.TemplateWidget):
  """Base class for all the site's pages, sets up outline and navbar"""
  def __init__(self, req):
    self.navbar = NavBar(req, self.title).embed()
    self.outline = Outline(req, title=self.title, body=self.embed())

  def write(self, req):
    self.outline.write(req)


class kw:
  def __init__(self, **kw):
    vars(self).update(kw)


# ========================================================================== #
# CGI handler
# ========================================================================== #

def handle_cgi(Page):
  from widgets import driver_cgi
  req = driver_cgi.Request()
  req.write('Content-Type: text/html\r\n\r\n')
  Page(req).write(req)


# ========================================================================== #
# Mod_Python handler
# ========================================================================== #

import os.path

def handler(mp_req):
  global apache, driver_mod_python
  from mod_python import apache
  from widgets import driver_mod_python

  # based on publisher.py
  path, module_name =  os.path.split(mp_req.filename)
  module_name, module_ext = os.path.splitext(module_name)
  try:
    module = apache.import_module(module_name, path=[path])
  except ImportError:
    raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

  mp_req.content_type = 'text/html'

  req = driver_mod_python.Request(mp_req)
  page = module.Page(req)
  page.write(req)

  return apache.OK
