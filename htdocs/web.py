import widgets
from widgets.driver_ezt import Template

import time
import calendar
import re


# location of these pages on server
ROOT = "/"


### At the moment, it's convenient to write these templates in python strings.
### Should probably push them out to files if the site grows
class Outline(widgets.TemplateWidget):
  root = ROOT
  template = Template(
"""|
<!DOCTYPE html>
<meta charset="UTF-8">
<title>Russell Yanofsky - [title]</title>
<style type="text/css">
<!--

body {
  margin: 0px;
  padding: 0px;
  background-image: url([root]media/tri.png);
  background-repeat: no-repeat;
  font-family: Trebuchet MS, Arial, Helvetica, sans-serif;
}

img {
  border: none;
}

td {
  vertical-align: top;
}

a {
  text-decoration: none;
  color: #0f18ec;
}

#fronthead {
  text-align: left;
  margin-top: 3em;
  margin-bottom: 3em;
}

.head {
  font-size: xx-large;
  font-weight: bold;
}

.subhead {
  font-size: large;
  font-style: italic;
}

#footer {
  margin-top: 3em;
  text-align: right;
}

.outlink {
  font-style: italic;
}

#code-intro {
  margin-bottom: 1em;
}

#code-controls {
  background: white;
  border-style: solid;
  border-color: black;
  border-width: 1px 2px 2px 1px;
  margin-left: 1em;
  padding: 0.5em;
}

#code-submit {
  text-align: center;
}

.code-pager {
  margin-bottom: 1em;
  text-align: right;
  font-weight: bold;
}

.code-project {
  border-style: solid;
  border-color: black;
  border-width: 1px;
  margin-bottom: 1em;
}

#code-sloc {
  margin-bottom: 1em;
  text-align: center;
  font-size: smaller;
  font-style: italic;
}

-->
</style>
<body>

[for signs]|
  [if-any signs.active]|
  [else]|
    |<a href="[signs.href]"><img src="[signs.src]" id="[signs.id]" alt="[signs.title]" style="width: [signs.width]px; height: [signs.height]px; position: absolute; top: [signs.top]px; left: [signs.left]px;" /></a>
  [end]|
[end]|

<div id="rect" style="background-color: #ff5509; width: [rect_width]px; height: [rect_height]px; position: absolute; top: [rect_pos]px; left: [rect_pos]px;"></div>

<div style="margin-top: 0px; margin-left: [tri_width]px; margin-right: [rect_pos]px; margin-bottom: [rect_pos]px;">

<div id="grect" style="background-image: url([root]media/grect.png); width: [rect_swidth]px; height: [rect_height]px;  margin-left: auto; margin-right: 0px; margin-top: [rect_pos]px; margin-bottom: [rect_pos]px;">
[for signs]|
  [if-any signs.active]|
    |<img src="[signs.src]" id="gsign" alt="[signs.title]" style="width: [signs.width]px; height: [signs.height]px; position: relative; top: [signs.top]px; left: [signs.left]px;" />
  [end]|
[end]|
</div>

<div id="load" style="position: absolute; right: [rect_pos]px; margin-top: [rect_pos]px; background-color: #FFFFCC; padding: 5px; border: 1px solid black; visibility: hidden"></div>

<script type="text/javascript">
<!--
(function(){

function Sign(title, id, href, src, width, height, hat, heels, corn, active)
{
  this.title = title;
  this.id = id;
  this.href = href;
  this.src = src;
  this.width = width;
  this.height = height;
  this.hat = hat;
  this.heels = heels;
  this.corn = corn;
  this.active = active;

  this.left = null;
  this.top = null;
  this.curLeft = null;
  this.curTop = null;
  this.clickLeft = null;
  this.clickTop = null;
  this.clickTime = null;
  this.moveTime = null;
  this.retract = null;
}

function Animation(signs, triWidth, triHeight, rectWidth, rectHeight,
                   rectSWidth, rectPos, signSpacing, rectId, grectId,
                   gsignId, statusId, contentsId)
{
  this.signs = signs;
  this.triWidth = triWidth;
  this.triHeight = triHeight;
  this.rectWidth = rectWidth;
  this.rectHeight = rectHeight;
  this.rectSWidth = rectSWidth;
  this.rectPos = rectPos;
  this.signSpacing = signSpacing;

  this.req = http_req();
  this.timer = null;
  this.loadUrl = null;

  this.rect = document.getElementById(rectId);
  this.grect = document.getElementById(grectId);
  this.gsign = document.getElementById(gsignId);
  this.status = document.getElementById(statusId);
  this.contentsId = contentsId;

  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];
    sign.elem = document.getElementById(sign.id);
    if (sign.elem)
    {
      sign.aelem = sign.elem.parentNode;
    }
    else
    {
      var ae = sign.aelem = document.createElement("a");
      ae.href = sign.href;
      var se = sign.elem = document.createElement("img");
      se.src = sign.src;
      se.style.position = "absolute";
      se.style.width = sign.width + "px";
      se.style.height = sign.height + "px";
      se.style.left = (this.grect.offsetLeft + (this.rectSWidth-sign.width) / 2)
                      + "px";
      se.style.top = (this.rectPos + (this.rectHeight-sign.height) / 2)
                     + "px";
      se.style.visibility = "hidden";
      ae.appendChild(se);
      document.body.insertBefore(ae, this.rect);
    }

    sign.aelem.onclick = this.onclick.bind(this, sign);

    sign.curLeft = sign.elem.offsetLeft;
    sign.curTop = sign.elem.offsetTop;
  }

  window.onresize = this.onresize.bind(this);

  this.setpos();
  this.draw_lines();
}

Animation.prototype.move = function(nsign)
{
  var now = date_now();
  var asign = null;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];

    if (!sign.retract)
    {
      sign.clickLeft = sign.curLeft;
      sign.clickTop = sign.curTop;
      sign.clickTime = now;
    }
    sign.moveTime = now + 1000;

    if (sign === nsign)
      sign.active = true;
    else if (sign.active)
    {
      sign.active = false;
      sign.retract = true;
      asign = sign;
    }
  }
  this.setpos();
  this.start_timer();
  this.start_load(nsign.href);
  this.hide_active(asign, nsign);
}

Animation.prototype.setpos = function()
{
  var j = 0;
  var y = this.rectPos + this.rectHeight;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];
    var se = sign.elem;
    if (sign.active)
    {
      sign.left = this.grect.offsetLeft + (this.rectSWidth - sign.width) / 2;
      sign.top = this.rectPos + (this.rectHeight - sign.height) / 2;
    }
    else
    {
      y += this.signSpacing;
      y -= sign.hat;
      sign.left = ((this.triWidth-(y+sign.corn)*this.triWidth/this.triHeight)/2
                 - se.offsetWidth / 2);
      sign.top = y;
      y -= sign.heels;
      y += sign.height;
      j += 1
    }
  }
}

Animation.prototype.tick = function()
{
  var now = date_now();
  var kill = true;
  var asign = null;
  var left;
  var top;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];
    var se = sign.elem;
    var ss = se.style;

    if (sign.active) asign = sign;

    var left, top;

    if (now >= sign.moveTime)
    {
      left = sign.left;
      top = sign.top;
    }
    else if (sign.retract)
    {
      kill = false;
      left = this.rectPos + (this.rectWidth - sign.width) / 2;
      top = this.rectPos + (this.rectHeight - sign.height) / 2;
      var t = (now - sign.clickTime) / 500.0;
      t = t * t;
      if (t >= 1.0)
      {
        sign.retract = false;
        sign.clickTime = now;
        sign.clickLeft = left;
        sign.clickTop = top;
      }
      else
      {
        left = sign.clickLeft + t * (left - sign.clickLeft);
        top = sign.clickTop + t * (top - sign.clickTop);
      }
    }
    else
    {
      kill = false;
      left = sign.clickLeft + (sign.left - sign.clickLeft)
             * (now - sign.clickTime) / (sign.moveTime - sign.clickTime);
      top = sign.clickTop + (sign.top - sign.clickTop)
            * (now - sign.clickTime) / (sign.moveTime - sign.clickTime);
    }

    sign.curLeft = left;
    sign.curTop = top;
    ss.left = left + "px";
    ss.top = top + "px";
  }
  this.draw_lines();
  if (kill)
  {
    this.kill_timer();
    this.show_active(asign);
    this.finish_load();
  }
}

Animation.prototype.hide_active = function(sign, nsign)
{
  sign.elem.style.left = sign.curLeft + "px";
  sign.elem.style.top = sign.curTop + "px";
  sign.elem.style.visibility = "visible";
  this.gsign.style.visibility = "hidden";
}

Animation.prototype.show_active = function(sign)
{
  this.gsign.src = sign.src;
  this.gsign.style.width = sign.width + "px";
  this.gsign.style.height = sign.height + "px";
  this.gsign.style.left = ((this.rectSWidth - sign.width) / 2) + "px";
  this.gsign.style.top = ((this.rectHeight - sign.height) / 2) + "px";
  this.gsign.style.visibility = "visible";
  sign.elem.style.visibility = "hidden";
}

Animation.prototype.draw_lines = function()
{
  if (!this.dots)
  {
    this.dots = document.createElement("div");
    this.dots.style.position = "absolute";
    this.dots.style.left = "0px";
    this.dots.style.top = "0px";

    document.body.insertBefore(this.dots, document.body.firstChild);
    this.ndots = 0
  }

  var x1, y1, x2, y2;

  var SQDIST = 12;
  var SQSIZE = 10;

  var idots = 0;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];

    x2 = sign.curLeft + sign.width / 2;
    y2 = sign.curTop + sign.height / 2;

    if (x2 > this.rectPos + this.rectWidth)
    {
      x1 = this.rectPos + this.rectWidth + SQDIST - SQSIZE / 2;
      y1 = this.rectPos + this.rectHeight + SQDIST - SQSIZE / 2;
      if (y2 < y1) y1 = y2;
    }
    else
    {
      x1 = x2;
      y1 = this.rectPos + this.rectHeight + SQDIST - SQSIZE / 2;
    }

    var x = x1;
    var y = y1;
    for (;;)
    {
      if (idots >= this.ndots)
      {
        ++this.ndots;

        var dot = document.createElement("div");

        // IE6 hack needed to set div height < line height
        dot.appendChild(document.createComment(""));

        dot.style.background = "black";
        dot.style.position = "absolute";
        dot.style.width = "10px";
        dot.style.height = "10px";
        dot.style.lineHeight = "1px";
        dot.style.left = (x - SQSIZE / 2) + "px";
        dot.style.top = (y - SQSIZE / 2) + "px";
        this.dots.appendChild(dot);
      }
      else
      {
        var dot = this.dots.childNodes[[]idots];
        dot.style.visibility = "visible";
        dot.style.left = (x - SQSIZE / 2) + "px";
        dot.style.top = (y - SQSIZE / 2) + "px";
      }

      var dx = x2 - x;
      var dy = y2 - y;

      if ((dx < 0 ? -dx : dx) > (dy < 0 ? -dy : dy))
      {
        var mx = dx < 0 ? -SQDIST : SQDIST;
        x += mx;
        y += mx * dy / dx;
      }
      else
      {
        var my = dy < 0 ? -SQDIST : SQDIST;
        x += dy ? my * dx / dy : 0;
        y += my;
      }
      ++idots;

      if ((dx < 0 ? -dx : dx) < SQDIST && (dy < 0 ? -dy : dy) < SQDIST)
        break;
    }
  }

  for (; idots < this.ndots; ++idots)
  {
    var dot = this.dots.childNodes[[]idots];
    dot.style.visibility = "hidden";
  }
}

Animation.prototype.start_timer = function()
{
  if (!this.timer)
    this.timer = setInterval(this.tick.bind(this), 20);
}

Animation.prototype.kill_timer = function()
{
  if (this.timer)
  {
    clearInterval(this.timer);
    this.timer = null;
  }
}

Animation.prototype.start_load = function(url)
{
  if (this.req)
  {
    this.loadUrl = null;
    this.req.abort();
  }

  this.loadUrl = url;

  if (this.req)
  {
    this.set_status(url)
    this.req.open("GET", url + "?plain=1", true);
    this.req.onreadystatechange = this.state_change.bind(this);
    this.req.send(null);
  }
}

Animation.prototype.finish_load = function()
{
  if (this.req)
  {
    if (!this.loadUrl && !this.timer)
    {
      this.set_status();
      document.getElementById(this.contentsId).innerHTML = this.req.responseText;
    }
  }
  else
  {
    window.location = this.load;
  }
}

Animation.prototype.state_change = function()
{
  if (!this.loadUrl) return;

  if (this.req.readyState === 4 |||| this.req.readyState === "complete")
  {
    var status, statusText;
    try
    {
      status = this.req.status;
      statusText = this.req.statusText;
    }
    catch(e)
    {}

    if (status === 200)
    {
      this.set_status(this.loadUrl, "Done.");
      this.loadUrl = null;
      this.finish_load();
    }
    else if (status)
      this.set_status(this.loadUrl, "Error: " + status + " " + statusText);
    else
      this.set_status(this.loadUrl, "Error: connection failed");
  }
  else
  {
    var status = "Unrecognized status";
    if (this.req.readyState === 0 |||| this.req.readyState === "uninitialized")
      status = "Initializing...";
    else if (this.req.readyState === 1 |||| this.req.readyState === "loading")
      status = "Retrieving headers...";
    else if (this.req.readyState === 2 |||| this.req.readyState === "loaded")
      status = "Retrieving contents...";
    else if (this.req.readyState === 3 |||| this.req.readyState === "interactive")
      status = "Downloading contents...";
    this.set_status(this.loadUrl, status);
  }
}

Animation.prototype.set_status = function(url, message)
{
  if (url)
  {
    this.status.innerHTML = ('Loading <a href="' + url + '">' + url + "<\\/a>"
                             + (message ? "<br /><em>" + message + "<\\/em>"
                                        : ""));
    this.status.style.visibility = "visible";
  }
  else
  {
    this.status.style.visibility = "hidden";
  }
}

Animation.prototype.go = function(id, url)
{
  var elem = document.getElementById(id);
  var sign;
  for (var i = 0; i < this.signs.length; ++i)
  {
    sign = this.signs[[]i];
    if (sign.elem == elem)
    {
      this.move(sign);
      return false;
    }
  }
}

Animation.prototype.onclick = function(sign)
{
  this.move(sign);
  return false;
}

Animation.prototype.onresize = function()
{
  this.setpos();
  if (!this.timer)
  {
    for (var i in this.signs)
    {
      var sign = this.signs[[]i];
      sign.curLeft = sign.left;
      sign.curTop = sign.top;
    }
    this.draw_lines();
  }
}

function date_now()
{
  if (Date.now)
    return Date.now();
  else
    return (new Date).getTime();
}

function http_req()
{
  if (window.XMLHttpRequest)
    return new XMLHttpRequest;
  else if (window.ActiveXObject)
    return new ActiveXObject("Microsoft.XMLHTTP")
}

window.anim = new Animation([[]|
[for signs]|
  [if-index signs first][else],
  |                             |
  [end]|
  |new Sign("[signs.title]", "[signs.id]", "[signs.href]", "[signs.src]", |
            [signs.width], [signs.height], |
            [signs.hat], [signs.heels], [signs.corn], |
            [if-any signs.active]true[else]false[end])|
[end]],
  |                            |
  [tri_width], [tri_height], [rect_width], [rect_height], [rect_swidth], |
  [rect_pos], [sign_spacing], "rect", "grect", "gsign", "load", "contents");

}());
// -->
</script>

<div id="contents">
[body]
</div>
</div>
</body>""", compress_whitespace=0, trim_whitespace=1)

  def __init__(self, *args, **kwargs):
    widgets.TemplateWidget.__init__(self, *args, **kwargs)
    self.tri_width = 271
    self.tri_height = 1801
    self.rect_width = 199
    self.rect_height = 150
    self.rect_swidth = 222

    # rectangle is centered in top of triangle
    self.rect_pos = ((self.tri_height * self.tri_width
                      - self.rect_height * self.tri_width
                      - self.rect_width * self.tri_height)
                     / (2 * self.tri_height + self.tri_width))

    self.signs = [ Sign("Home", "home", "index.py", "media/home.png",
                        143, 60, 7, 13, 7),
                   Sign("Code", "code", "code.py", "media/code.png",
                        115, 60, 5, 16, 60),
                   Sign("Resume", "resume", "resume.py", "media/resume.png",
                        149, 48, 6, 10, 48),
                   Sign("Links", "links", "links.py", "media/links.png",
                        127, 61, 8, 25, 61) ] # 25 -> 19

    self.sign_spacing = 40

    i = j = 0
    y = self.rect_pos + self.rect_height
    for sign in self.signs:
      if self.title == sign.title:
        sign.active = "yes"
        sign.left = (self.rect_swidth - sign.width) / 2
        sign.top = (self.rect_height - sign.height) / 2
      else:
        sign.active = None
        y += self.sign_spacing
        y -= sign.hat
        sign.top = y
        sign.left = ((self.tri_width
                      -(y+sign.corn)*self.tri_width/self.tri_height)/2
                      - sign.width / 2)
        y -= sign.heels
        y += sign.height
        j += 1
      i += 1


class Sign:
  def __init__(self, title, id, href, src, width, height, hat, heels, corn):
    self.title = title
    self.id = id
    self.href = href
    self.src = src
    self.width = width
    self.height = height
    self.top = None
    self.left = None
    self.hat = hat # lower top corner from top
    self.heels = heels # higher bottom corner from bottom
    self.corn = corn # height or right edge


class Footer(widgets.TemplateWidget):
  root = ROOT
  template = Template(
"""<div id="footer">
  <hr />
  <a href="[date_href]" title="Last Modified">[date]</a>
  <a href="mailto:[mail]" title="Email"><img src="[root]media/mail.png" alt="Email" /></a>
  <a href="[href]" title="Current Page Link"><img src="[root]media/link.png" alt="Current Page" /></a>
  </div>""")

  def __init__(self, req, **kwargs):
    widgets.TemplateWidget.__init__(self, req, **kwargs)
    self.href = (req.request_uri() or "").replace("?plain=1", "")


class BasePage(widgets.TemplateWidget):
  """Base class for all the site's pages, sets up outline and navbar"""
  DATE = None
  root = ROOT

  def __init__(self, req):
    self.navbar = "";
    self.footer = Footer(req, date =self.reformat_date(self.DATE),
                         date_href="/viewvc.py/site/trunk/htdocs%s?view=log"
                                   % req.script_name(),
                         mail="russ@yanofsky.org").embed()
    if req.get.getfirst("plain"):
      self.outline = None
    else:
      self.outline = Outline(req, body=self.embed(), title=self.title)

  def write(self, req):
    if self.outline:
      self.outline.write(req)
    else:
      widgets.TemplateWidget.write(self, req)

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


def ezt(string):
  # Preference is to keep index.py/links.py pages frozen in place from 2006
  # since they don't serve any purpose, and would be ridiculous to modernize.
  # A few external links are broken and can be patched though.
  string = string.replace("http://www.evilive.net/",
                          "https://web.archive.org/web/20050204121854/http://www.evilive.net/")
  string = string.replace("http://www.cs.washington.edu/homes/klee/misc/slashdot.html",
                          "http://web.archive.org/web/20120428034140/http://www.cs.washington.edu/homes/klee/misc/slashdot.html")
  string = string.replace("http://memepool.com/",
                          "https://en.wikipedia.org/wiki/Memepool")
  string = string.replace('href="/ssh/ssh.html"', 'href="/ssh/"')

  return Template(string)


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
