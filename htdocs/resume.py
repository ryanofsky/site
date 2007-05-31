#!/usr/bin/env python
import os.path
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Resume"
  template = web.ezt(
"""[navbar]
<p>Resume in assorted formats:</p>
<ul>
  <li>HTML ([file "resume.html"])</li>
  <li>Text ([file "resume.txt"])</li>
  <li>PDF ([file "resume.pdf"])</li>
  <li>Postscript ([file "resume.ps"])</li>
  <li>OpenOffice ([file "resume.odt"])</li>
  <li>Microsoft Word ([file "resume.doc"])</li>
</ul>

[footer]""")

  def file(self, out, path):
    size = str(os.path.getsize(os.path.join(DIR, "resume", path)))
    out.write('<a href="resume/%s">%s</a>, %s bytes'
              % (path, path, commify(size)))


def commify(number):
  """Format a non-negative integer with commas"""
  n = str(number)
  l = len(n)
  return ','.join((l%3 and [n[:l%3]] or [])
                  + [n[i:i+3] for i in range(l%3, l, 3)])

DIR = os.path.dirname(__file__)

if __name__ == '__main__':
  web.handle_cgi(Page)
