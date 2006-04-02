import widgets
from widgets.driver_ezt import Template as ezt

import time
import calendar
import re


# location of these pages on server
ROOT = "/"


### At the moment, it's convenient to write these templates in python strings.
### Should probably push them out to files if the site grows
class Outline(widgets.TemplateWidget):
  template = ezt(
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>Russell Yanofsky - [title]</title>
<link rel="stylesheet" href="media/styles.css" type="text/css" />
</head>
<body>
<div id="main">
[body]
</div>
</body>
</html>""")


class NavBar(widgets.TemplateWidget):
  root = ROOT
  template = ezt(
"""<script type="text/javascript">
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
<div id="navbar">

[for links]
[define href][is caption links.caption][else]yes[end][end]
[define mousey] onmouseover="setCaption('[if-any href]&lt;em>[links.caption]&lt;/em>[else][links.caption][end]')" onmouseout="revertCaption()"[end]
[define img]<img src="[root][if-any href][links.img][else][links.imgglow][end]" width="[links.width]" height="[links.height]" alt="[links.caption]" />[end]
[if-any href]<a href="[root][links.href]"[mousey]>[img]</a>[else][img][end]
[end]

<div id="caption">[caption]</div>

</div>
""")

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


class Footer(widgets.TemplateWidget):
  root = ROOT
  template = ezt(
"""<div id="footer">
  <hr />
  <a href="[date_href]" title="Last Modified">[date]</a>
  <a href="mailto:[mail]" title="Email"><img src="[root]media/mail.png" alt="Email" /></a>
  </div>""")


class BasePage(widgets.TemplateWidget):
  """Base class for all the site's pages, sets up outline and navbar"""
  DATE = None
  root = ROOT

  def __init__(self, req):
    self.navbar = NavBar(req, self.title).embed()
    self.footer = Footer(req, date =self.reformat_date(self.DATE),
                         date_href="/viewvc.py/site/trunk/htdocs%s?view=log"
                                   % req.script_name(),
                         mail="russell.yanofsky@us.army.mil").embed()
    self.outline = Outline(req, body=self.embed(), title=self.title)

  def write(self, req):
    self.outline.write(req)

  def reformat_date(self, date):
    if date is None:
      return None
    m = re.match(r"\$Date: (\d{4})-(\d{2})-(\d{2}) "
                 r"(\d{2}):(\d{2}):(\d{2}) ([+-]\d{4}) .*\$$", 
                 date)
    if not m:
      return None
    year, month, day, hour, min, sec, offset = map(int, m.groups())
    if offset < 0:
      offset = -60 * ((-offset % 100) + 60 * (-offset // 100))
    else:
      offset = 60 * ((offset % 100) + 60 * (offset // 100))
    ticks = (calendar.timegm((year, month, day, hour, min, sec, 0, 0, 0))
             - offset)
    return time.strftime('%a %b %d %H:%M:%S UTC %Y', time.gmtime(ticks))

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
  path, module_name = os.path.split(mp_req.filename)
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
