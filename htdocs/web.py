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
<title>[doc_title]</title>
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

function Sign(info, active)
{
  this.info = info;
  this.active = active;
  this.curLeft = null;
  this.curTop = null;
  this.finalLeft = null;
  this.finalTop = null;
  this.startLeft = null;
  this.startTop = null;
  this.startTime = null;
  this.retracting = null;
}

function Animation(signs, info)
{
  this.signs = signs;
  this.info = info;

  this.req = http_req();
  this.loadUrl = window.location.pathname;
  this.loadDestination = null;
  this.loadPending = false;

  this.animationStarted = null;
  this.timer = null;

  this.rect = document.getElementById(info.rectId);
  this.grect = document.getElementById(info.grectId);
  this.gsign = document.getElementById(info.gsignId);
  if (!this.gsign)
  {
    // Create top stationary sign element if there isn't one already in the
    // static HTML (needed for pages like edit.py that don't have sign links
    // pointing at them).
    this.gsign = document.createElement("img");
    this.gsign.style.position = "relative";
    this.gsign.style.visibility = "hidden";
    this.grect.appendChild(this.gsign);
  }
  this.status = document.getElementById(info.statusId);

  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];

    sign.elem = document.getElementById(sign.info.id);
    if (!sign.elem)
    {
      // Create LHS sign element if there isn't one in the static HTML (because
      // the sign is active and located on top instead of on the left).
      sign.elem = document.createElement("img");
      sign.elem.src = sign.info.src;
      sign.elem.style.position = "absolute";
      sign.elem.style.width = sign.info.width + "px";
      sign.elem.style.height = sign.info.height + "px";
      // Compute top/left position even though element is not visible so
      // curLeft/curTop will be initialized correctly below and animation code
      // will use the right start position.
      sign.elem.style.left = (this.grect.offsetLeft
                              + (this.info.rectSWidth - sign.info.width) / 2
                              + "px");
      sign.elem.style.top = (this.info.rectPos
                             + (this.info.rectHeight - sign.info.height) / 2
                             + "px");
      sign.elem.style.visibility = "hidden";

      var sa = document.createElement("a");
      sa.href = sign.info.href;
      sa.appendChild(sign.elem);
      document.body.insertBefore(sa, this.rect);
    }

    sign.aelem = sign.elem.parentNode;
    sign.aelem.onclick = this.onclick.bind(this, sign.info.href);

    sign.curLeft = sign.elem.offsetLeft;
    sign.curTop = sign.elem.offsetTop;

    if (sign.active) this.loadUrl = sign.info.href;
  }

  this.initialHref = this.loadUrl;

  window.onhashchange = this.onhashchange.bind(this);
  window.onresize = this.onresize.bind(this);

  this.updateSigns(true /* immediate */);
  this.updateLayout();
  this.updateStyle();
}

Animation.prototype.getCurrentHref = function()
{
  var hashHref = window.location.hash.substring(1);
  return /\.py\\b/.test(hashHref) ? hashHref : this.initialHref;
}

Animation.prototype.setCurrentHref = function(href)
{
  if (!this.req)
    this.initialHref = href;
  else
    window.location.hash = "#" + href;
}

Animation.prototype.updateSigns = function(immediate)
{
  var href = this.getCurrentHref();

  // Don't do anything if the right URL is already loaded.
  if (this.loadUrl === href) return;

  this.loadUrl = href;

  var now = date_now();
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];
    var prevActive = sign.active;
    sign.active = sign.info.href === href;
    if (sign.active |||| !sign.retracting)
    {
      sign.startLeft = sign.curLeft;
      sign.startTop = sign.curTop;
      sign.startTime = now;
    }
    sign.retracting = !immediate && !sign.active
                      && (prevActive |||| sign.retracting);
  }

  // Call startAnimation before startLoad, so this.animationStarted will be set.
  // Otherwise after a really fast response, loading code waiting for the
  // animation to complete might think the animation is finished before it
  // starts.
  if (!immediate) this.startAnimation(now);
  this.startLoad();
}

Animation.prototype.updateLayout = function()
{
  var j = 0;
  var y = this.info.rectPos + this.info.rectHeight;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];
    if (sign.active)
    {
      sign.finalLeft = this.grect.offsetLeft
                       + (this.info.rectSWidth - sign.info.width) / 2;
      sign.finalTop = (this.info.rectPos
                       + (this.info.rectHeight - sign.info.height) / 2);
    }
    else
    {
      y += this.info.signSpacing;
      y -= sign.info.hat;
      sign.finalLeft = (this.info.triWidth
                        - (y + sign.info.corn)
                          * this.info.triWidth / this.info.triHeight
                        - sign.elem.offsetWidth) / 2;
      sign.finalTop = y;
      y -= sign.info.heels;
      y += sign.info.height;
      j += 1
    }
  }
}

Animation.prototype.updateStyle = function()
{
  var now = date_now();
  var duration = 1000;
  if (this.animationStarted)
  {
    var finishTime = this.animationStarted + duration;
    if (now >= finishTime) this.animationStarted = null;
  }

  var asign = null;
  for (var i = 0; i < this.signs.length; ++i)
  {
    var sign = this.signs[[]i];

    if (sign.active) asign = sign;

    var left, top;

    if (!this.animationStarted)
    {
      left = sign.finalLeft;
      top = sign.finalTop;
      sign.retracting = false;
    }
    else if (sign.retracting)
    {
      left = this.info.rectPos + (this.info.rectWidth - sign.info.width) / 2;
      top = this.info.rectPos + (this.info.rectHeight - sign.info.height) / 2;
      var t = (now - sign.startTime) / duration * 2;
      t = t * t;
      if (t >= 1.0)
      {
        sign.retracting = false;
        sign.startTime = now;
        sign.startLeft = left;
        sign.startTop = top;
      }
      else
      {
        left = sign.startLeft + t * (left - sign.startLeft);
        top = sign.startTop + t * (top - sign.startTop);
      }
    }
    else
    {
      left = sign.startLeft + (sign.finalLeft - sign.startLeft)
             * (now - sign.startTime) / (finishTime - sign.startTime);
      top = sign.startTop + (sign.finalTop - sign.startTop)
            * (now - sign.startTime) / (finishTime - sign.startTime);
    }

    sign.curLeft = left;
    sign.curTop = top;
    sign.elem.style.left = left + "px";
    sign.elem.style.top = top + "px";
    sign.elem.style.visibility = !sign.active |||| this.animationStarted
                                 ? "visible" : "hidden";
  }

  this.drawLines();

  if (asign && !this.animationStarted)
  {
    this.gsign.src = asign.info.src;
    this.gsign.style.width = asign.info.width + "px";
    this.gsign.style.height = asign.info.height + "px";
    this.gsign.style.left = ((this.info.rectSWidth - asign.info.width) / 2
                             + "px");
    this.gsign.style.top = ((this.info.rectHeight - asign.info.height) / 2
                            + "px");
    this.gsign.style.visibility = "visible";
  }
  else
  {
    this.gsign.style.visibility = "hidden";
  }
}

Animation.prototype.drawLines = function()
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

    x2 = sign.curLeft + sign.info.width / 2;
    y2 = sign.curTop + sign.info.height / 2;

    if (x2 > this.info.rectPos + this.info.rectWidth)
    {
      x1 = this.info.rectPos + this.info.rectWidth + SQDIST - SQSIZE / 2;
      y1 = this.info.rectPos + this.info.rectHeight + SQDIST - SQSIZE / 2;
      if (y2 < y1) y1 = y2;
    }
    else
    {
      x1 = x2;
      y1 = this.info.rectPos + this.info.rectHeight + SQDIST - SQSIZE / 2;
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

Animation.prototype.startAnimation = function(now)
{
  this.animationStarted = now;
  this.updateLayout();
  if (!this.timer)
    this.timer = setInterval(this.timerTick.bind(this), 20);
}

Animation.prototype.timerTick = function()
{
  this.updateStyle();
  if (!this.animationStarted)
  {
    clearInterval(this.timer);
    this.timer = null;
    this.finishLoad();
  }
}

Animation.prototype.startLoad = function()
{
  if (this.req)
  {
    this.setLoadStatus(this.loadUrl);
    this.req.abort();
    this.req.open("GET", this.loadUrl + "?plain=1", true);
    this.req.onreadystatechange = this.loadStateChange.bind(this);
    this.req.send(null);
  }
  else
  {
    this.loadPending = true;
    this.finishLoad();
  }
}

Animation.prototype.finishLoad = function()
{
  if (this.animationStarted |||| !this.loadPending) return;

  if (this.req)
  {
    if (this.loadDestination !== null)
    {
      this.setLoadStatus();
      this.loadDestination.innerHTML = this.req.responseText;
      var outline = this.loadDestination.firstChild;
      var doc_title = outline && outline.getAttribute("data-doc-title");
      if (doc_title) document.title = doc_title;
      this.loadPending = false;
    }
  }
  else
  {
    window.location = this.loadUrl;
    this.loadPending = false;
  }
}

Animation.prototype.setLoadDestination = function(contentsId)
{
  this.loadDestination = document.getElementById(contentsId) |||| undefined;
  this.finishLoad();
}

Animation.prototype.loadStateChange = function()
{
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
      this.setLoadStatus(this.loadUrl, "Done.");
      this.loadPending = true;
      this.finishLoad();
    }
    else if (status)
      this.setLoadStatus(this.loadUrl, "Error: " + status + " " + statusText);
    else
      this.setLoadStatus(this.loadUrl, "Error: connection failed");
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
    this.setLoadStatus(this.loadUrl, status);
  }
}

Animation.prototype.setLoadStatus = function(url, message)
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

Animation.prototype.click = function(target, event)
{
  var href = target.getAttribute("href");
  return this.onclick(href, event);
}

Animation.prototype.onclick = function(href, event)
{
  // Let the browser handle right and middle clicks by itself.
  if (event && event.which > 1) return true;

  this.setCurrentHref(href);
  this.updateSigns();
  return false;
}

Animation.prototype.onhashchange = function()
{
  this.updateSigns();
  return true;
}

Animation.prototype.onresize = function()
{
  this.updateLayout();
  this.updateStyle();
  return true;
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

window.anim = new Animation([[][for signs]
  new Sign({title: "[signs.title]", id: "[signs.id]", href: "[signs.href]",
            src: "[signs.src]", width: [signs.width], height: [signs.height],
            hat: [signs.hat], heels: [signs.heels], corn: [signs.corn]}, |
           [if-any signs.active]true[else]false[end])|
           [if-index signs last][else],[end][end]],
  {triWidth:[tri_width], triHeight: [tri_height], |
   | rectWidth: [rect_width], rectHeight: [rect_height],
   rectSWidth: [rect_swidth], rectPos: [rect_pos], signSpacing: [sign_spacing],
   rectId: "rect", grectId: "grect", gsignId: "gsign", statusId: "load"});
}());
// -->
</script>

<div id="contents">
[body]
</div>

<script type="text/javascript">
<!--
anim.setLoadDestination("contents");
// -->
</script>

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


class PlainOutline(widgets.TemplateWidget):
  template = Template('<div data-doc-title="[doc_title]">[body]</div>')


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
    outline_cls = PlainOutline if req.get.getfirst("plain") else Outline
    self.outline = outline_cls(req,
                               body=self.embed(),
                               title=self.title,
                               doc_title = "Russell Yanofsky - " + self.title)

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
  string = string.replace('href="/edit.py"',
                          'href="/edit.py" onclick="return anim.click(this, event)"')

  # For compatibility, replace old anim.go event handlers with anim.click event
  # handlers.
  string = re.sub("onclick=\"return anim\\.go\('.*?'\)\"",
                  "onclick=\"return anim.click(this, event)\"", string)
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
