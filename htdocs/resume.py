#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Resume"
  template = web.ezt(
"""[navbar]
<p>Resume in assorted formats:</p>
<ul>
  <li>HTML (<a href="resume/resume.html">resume.html</a>, 9,800 bytes)</li>
  <li>Text (<a href="resume/resume.txt">resume.txt</a>, 2,801 bytes)</li>
  <li>PDF (<a href="resume/resume.pdf">resume.pdf</a>, 38,075 bytes)</li>
  <li>Postscript (<a href="resume/resume.ps">resume.ps</a>, 78,329 bytes)</li>
  <li>OpenOffice (<a href="resume/resume.odt">resume.odt</a>, 19,653 bytes</li>
  <li>Microsoft Word (<a href="resume/resume.doc">resume.doc</a>, 62,464 bytes)</li>
</ul>

<p>I'm looking for full-time programming work in New York City starting May 2006. A resume doesn't always provide the most complete picture of a person's qualifications, especially for someone like me, who has pretty good geek credentials, but not an abundance of relevant work experience. So I have a few more words to say here.</p>

<p>I've been more or less obsessed with computer programming ever since taking a high school class that taught <a href="http://en.wikipedia.org/wiki/Apple_IIe">IIe</a> <a href="http://en.wikipedia.org/wiki/BASIC">BASIC</a> and <a href="http://en.wikipedia.org/wiki/Assembly_language">assembly</a> on a set of ancient Apple computers, and <a href="http://en.wikipedia.org/wiki/Turbo_Pascal">Pascal</a> and <a href="http://en.wikipedia.org/wiki/Microsoft_QuickBASIC_compiler">QuickBASIC</a> on some less ancient PCs. Once obsessed, I taught myself <a href="http://en.wikipedia.org/wiki/C%2B%2B">C++</a> and <a href="http://en.wikipedia.org/wiki/Windows_API">Win32</a> programming, picked up <a href="http://en.wikipedia.org/wiki/Java_programming_language">Java</a> and <a href="http://en.wikipedia.org/wiki/POSIX">POSIX</a> programming through college coursework, learned <a href="http://en.wikipedia.org/wiki/PHP">PHP</a> and <a href="http://en.wikipedia.org/wiki/SQL">SQL</a> through a job developing web applications for my college, and fell in love with <a href="http://en.wikipedia.org/wiki/Python_programming_language">Python</a> after becoming involved with the <a href="http://viewvc.org/">ViewCVS</a> open-source project.</p>

<p>I love the mechanics of programming: struggling to put abstract concepts into concrete forms with clarity and precision, collaborating with people with similar interests and different strengths, puzzling over obscure sources to get into the heads of other developers. And I can't say that I love debugging, but I love the intuitive leaps you can make (after working on a project for a long enough time) that make most cases of it trivial. What I find most addictive about computers is that so many things, even the stupidest ones (like after a year of frustration, finally setting up software mixing so your Linux applications can play sound simultaneously, when of course it worked out of the box on Windows) feel like accomplishments. And some things, like doing the work you love while helping people solve problems they could not solve on their own, actually are.</p>
[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
