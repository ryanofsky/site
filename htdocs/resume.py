#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Resume"
  template = web.ezt(
"""[navbar]
<p>[[]This page is out of date, c. 2002]</p>
<p>Resume in assorted formats:</p>
<ul>
  <li>Microsoft Word (<a href="resume.doc">resume.doc</a>, 31,744 bytes)</li>
  <li>HTML (<a href="resume.htm">resume.htm</a>, 19,070 bytes)</li>
  <li>PDF (<a href="resume.pdf">resume.pdf</a>, 48,559 bytes)</li>
  <li>Postscript (<a href="resume.ps">resume.ps</a>, 109,844 bytes)</li>
</ul>
[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
