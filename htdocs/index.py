#!/usr/bin/env python
import web


class Page(web.BasePage):
  title = "Home"
  template = web.ezt(
"""[navbar]
<div class=notugly>
<p>Hi, I'm Russ Yanofsky, a computer science major at Columbia University's School of Engineering. This is my homepage, built to hold my resume, some links, and the source code for some programming projects I've worked on. </p>
</div>""")


if __name__ == '__main__':
  web.handle_cgi(Page)
