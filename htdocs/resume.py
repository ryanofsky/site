#!/usr/bin/env python
import web


class Page(web.BasePage):
  title = "Resume"
  template = web.ezt(
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


if __name__ == '__main__':
  web.handle_cgi(Page)
