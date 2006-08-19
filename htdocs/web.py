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
<style>
<!--
body {
  margin: 0px;
  padding: 0px;
  background-image: url(media/tri.png);
  background-repeat: no-repeat;
}

#main {
  margin-top: 0px;
  margin-left: [tri.width]px;
  margin-right: [rect.top]px;
  margin-bottom: [rect.top]20px;
}
-->
</style>

</head>
<body>

[for signs]
<a href="[signs.name].py" onclick="return false;"><img src="[signs.src]" id="sign_[signs.name]" style="width: [signs.width]px; height: [signs.height]px; position: absolute; top: [signs.top]px; left: [signs.left]px; border: none;" onclick="anim_click(this)" /></a>
[end]

<div id="rect" style="background-color: #ff5509; width: [rect.width]px; height: [rect.height]px; position: absolute; top: [rect.top]px; left: [rect.left]px;"></div>

<script>
<!--

function Sign(name, active, width, height, hat, heels, corn) 
{
  this.name = name;
  this.active = active;
  this.width = width;
  this.height = height;
  this.hat = hat;
  this.heels = heels;
  this.corn = corn;
  this.elem = document.getElementById("sign_" + name);
  this.left = null;
  this.top = null;
  this.curLeft = this.elem.offsetLeft;
  this.curTop = this.elem.offsetTop;
  this.clickLeft = null;
  this.clickTop = null;
  this.clickTime = null;
  this.moveTime = null;
}

function Animation(signs, timer_cb, req, onreadystatechange)
{
  this.signs = signs;
  this.timer = null;
  this.timer_cb = timer_cb;
  this.setpos = Animation_setpos
  this.load = null;
  this.req = req;
  this.onreadystatechange = onreadystatechange;
  this.start_timer = Animation_start_timer;
  this.kill_timer = Animation_kill_timer;
  this.start_load = Animation_start_load;
  this.state_change = Animation_state_change;
  this.finish_load = Animation_finish_load;
  this.draw_lines = Animation_draw_lines;
}

function Animation_setpos()
{
  var SP = 40;
  var j = 0;
  var rect = document.getElementById("rect");
  var grect = document.getElementById("grect");
  var y = rect.offsetTop + rect.offsetHeight;
  for (var i in this.signs)
  {
    var sign = this.signs[[]i];
    var se = sign.elem;
    if (sign.active)
    {
      sign.left = grect.offsetLeft + (grect.offsetWidth - se.offsetWidth) / 2;
      sign.top = grect.offsetTop + (grect.offsetHeight - se.offsetHeight) / 2;
    }
    else
    {
      y += SP;
      y -= sign.hat;
      sign.left = (([tri.width]-(y+sign.corn)*[tri.width]/[tri.height])/2
                 - se.offsetWidth / 2);
      sign.top = y;
      y -= sign.heels;
      y += sign.height;
      j += 1
    }
  }  
}

function Animation_start_timer()
{
  if (!this.timer)
    this.timer = setInterval(this.timer_cb, 1);
}

function Animation_kill_timer()
{
  if (this.timer)
  {
    clearInterval(this.timer);
    this.timer = null;
  }
}

function Animation_start_load(sign)
{
  if (this.req)
  {
    this.req.abort();
    this.req.open("GET", sign.name + ".py?plain=1", true);
    req.onreadystatechange = this.onreadystatechange;
    this.load = 0;
    this.req.send(null);
  }
  else
  {
    this.load = sign.name + ".py";
  }
}

function Animation_state_change(sign)
{
  if (this.req.readyState == 4 || this.req.readyState == "complete")
  {
    if (++this.load >= 2)
      document.getElementById("contents").innerHTML = this.req.responseText;
  }
}

function Animation_finish_load()
{
  if (this.req)
  {
    if (++this.load >= 2)
    {
      bum = this.req.responseText;
      document.getElementById("contents").innerHTML = bum;
    }
  }
  else
  {
    window.location = this.load;
  }
}

function Animation_draw_lines()
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
  for (i in this.signs)
  {
    var sign = this.signs[[]i];
    
    x2 = sign.curLeft + sign.width / 2;
    y2 = sign.curTop + sign.height / 2;
    
    if (x2 > [rect.left] + [rect.width])
    {
      x1 = [rect.left] + [rect.width] + SQDIST - SQSIZE / 2;
      y1 = [rect.top] + [rect.height] + SQDIST - SQSIZE / 2;
      if (y2 < y1) y1 = y2;
    }
    else
    {
      x1 = x2;
      y1 = [rect.top] + [rect.height] + SQDIST - SQSIZE / 2;
    }
    
    var x = x1;
    var y = y1;
    for (;;)
    {
      if (idots >= this.ndots)
      {
        ++this.ndots;
        //var dot = document.createElement("img");
        //dot.src = "media/black.png";

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

function anim_click(img)
{
  var now = date_now();
  for (var i in anim.signs)
  {
    var sign = anim.signs[[]i];
    if (sign.elem == img)
    {
      if (!sign.active)
      {
        anim.start_load(sign);
      }
      sign.active = true;
    }
    else if (sign.active)
      sign.active = false;
    sign.clickLeft = sign.curLeft;
    sign.clickTop = sign.curTop;
    sign.clickTime = now;
    sign.moveTime = now + 1000;
  }
  anim.setpos();
  anim.start_timer();
}

function anim_tick(img)
{
  var now = date_now();
  var kill = true;
  var left;
  var top;
  for (var i in anim.signs)
  {
    var sign = anim.signs[[]i];
    var se = sign.elem;
    var ss = se.style;

    if (now >= sign.moveTime)
    {
      var left = sign.left;
      var top = sign.top;
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
  anim.draw_lines();
  if (kill)
  {
    anim.kill_timer();
    anim.finish_load();
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

function anim_state_change()
{
  anim.state_change()
}

var req = http_req();

anim = new Animation(new Array(new Sign("home", true, 143, 60, 7, 13, 7),
                               new Sign("resume", false, 149, 48, 6, 10, 48),
                               new Sign("code", false, 115, 60, 5, 16, 60),
                               new Sign("links", false, 127, 61, 8, 25, 61)),
                     anim_tick, req, anim_state_change);

-->
</script>


<div id="main">
<div id="grect" style="width: [rect.width]px; height: [rect.height]px; background: #848484; margin-left: auto; margin-right: auto; margin-top: [rect.top]px; margin-bottom: [rect.top]px;">
</div>
<div id="contents">
[body]
</div>
</div>
</body>
</html>""")

  def __init__(self, *args, **kwargs):
    widgets.TemplateWidget.__init__(self, *args, **kwargs)
    self.tri = Image('media/tri.png', 271, 1801)
    self.rect = Image('media/rect.png', 199, 150)

    self.tri.top = self.tri.left = 0

    # center rectangle in top of triangle
    self.rect.top = self.rect.left = ((self.tri.height * self.tri.width
                                       - self.rect.height * self.tri.width
                                       - self.rect.width * self.tri.height)
                                      / (2 * self.tri.height + self.tri.width))
    
    self.signs = [ Sign("home", 143, 60, 7, 13, 7),
                   Sign("resume", 149, 48, 6, 10, 48),
                   Sign("code", 115, 60, 5, 16, 60),
                   Sign("links", 127, 61, 8, 25, 61) ] # 25 -> 19
    position_signs(self.signs, self.tri, self.rect, 0)    

class Image:
  def __init__(self, src, width, height):
    self.src = src
    self.width = width
    self.height = height
    self.top = None
    self.left = None


class Sign(Image):
  def __init__(self, name, width, height, hat, heels, corn):
    Image.__init__(self, "media/%s.png" % name, width, height)
    self.hat = hat # lower top corner from top
    self.heels = heels # higher bottom corner from bottom
    self.corn = corn # height or right edge
    self.name = name

def position_signs(signs, tri, rect, active):
  SP = 40
  i = j = 0
  y = rect.top + rect.height
  for sign in signs:
    if i == active:
      sign.active = "yes"
      sign.left = rect.left + (rect.width - sign.width) / 2
      sign.top = rect.top + (rect.height - sign.height) / 2
    else:
      sign.active = None
      y += SP
      y -= sign.hat 
      sign.top = y
      sign.left = ((tri.width-(y+sign.corn)*tri.width/tri.height)/2
                   - sign.width / 2)
      y -= sign.heels 
      y += sign.height
      j += 1
    i += 1


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
    self.navbar = ""; 
    self.footer = Footer(req, date =self.reformat_date(self.DATE),
                         date_href="/viewvc.py/site/trunk/htdocs%s?view=log"
                                   % req.script_name(),
                         mail="russell.yanofsky@us.army.mil").embed()
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
