#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Resume"
  template = web.ezt(
"""[navbar]
<p>Resume in assorted formats:</p>
<ul>
  <li>HTML (<a href="resume/resume.html">resume.html</a>, 9,690 bytes)</li>
  <li>Text (<a href="resume/resume.txt">resume.txt</a>, 2,720 bytes)</li>
  <li>PDF (<a href="resume/resume.pdf">resume.pdf</a>, 39,093 bytes)</li>
  <li>Postscript (<a href="resume/resume.ps">resume.ps</a>, 79,795 bytes)</li>
  <li>OpenOffice (<a href="resume/resume.odt">resume.odt</a>, 19,366 bytes</li>
  <li>Microsoft Word (<a href="resume/resume.doc">resume.doc</a>, 61,952 bytes)</li>
</ul>
[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
