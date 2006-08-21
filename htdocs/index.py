#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Home"
  template = web.ezt(
"""[navbar]
<div id="fronthead">
<div class="head">Russell Yanofsky</div>
<div class="subhead">In two dimensions!</div>
<hr />
</div>
<p>Welcome to a personal home page. Pretty neat, huh? There are a few interesting things here, notably source code and information about <a href="code.py" onclick="return anim.go('code')">programming projects</a> I've worked on. Also, my <a href="resume.py" onclick="return anim.go('resume')">resume</a>. I'm available for hire in three and even four dimensions.</p>
<p>If you're reading this page, you probably know me somehow. There are many ways this is possible. I grew up in Harrisburg, Pennsylvania, and went to college at <a href="http://www.columbia.edu/" class="outlink">Columbia University</a> in New York City. I also served in the US Army, and spent a year deployed to Iraq. I've been involved with a number of open source projects. Most of my coding contributions have been to the <a href="http://viewvc.org" class="outlink">ViewVC</a> project, but I've also made non-trivial contributions to the <a href="/rref/" class="outlink">GCC</a> and <a href="http://subversion.tigris.org/" class="outlink">Subversion</a> projects. I have a younger brother who goes to <a href="http://www.psu.edu" class="outlink">Penn State</a>, and a younger <a href="http://www.evilive.net/" class="outlink">sister</a>. I am currently 25 years old, but it is possible this may change.</p>

[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
