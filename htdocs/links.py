#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Links"
  template = web.ezt(
"""[navbar]
<h3>Reading</h3>

<p>
<a href="http://www.theatlantic.com/">Atlantic Monthly</a>,
<a href="http://www.wsj.com/">Wall Street Journal</a>,
<a href="http://www.sciam.com/">Scientific American</a>,
<a href="http://www.economist.com/">Economist</a>,
<a href="http://www.nytimes.com/">New York Times</a>,
<a href="http://www.washingtonpost.com/">Washington Post</a>,
<a href="http://www.csmonitor.com">Christian Science Monitor</a>,
<a href="http://slashdot.org/">Slashdot</a> (<a href="http://www.cs.washington.edu/homes/klee/misc/slashdot.html">or not</a>),
<a href="http://memepool.com/">Memepool</a>,
<a href="http://www.mcsweeneys.net/">McSweeneys</a>,
<a href="http://slate.msn.com/">Slate</a>
</p>

<h3>Useful Sites</h3>

<p>
<a href="http://www.google.com/">Google</a>,
<a href="http://groups.google.com/">Google Groups</a>,
<a href="http://www.google.com/univ/columbia">Google Columbia</a>,
<a href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a>,
<a href="http://www.onelook.com/">Dictionary</a>
</p>

<h3>Pages and Sites on this Machine</h3>
<ul>
  <li><a href="/cs1007/">/cs1007/</a>,
      <a href="/cs3156/">/cs3156/</a>,
      <a href="/cs4281/">/cs4281/</a> - web pages for classes</li>
  <li><a href="/cvcomputer/">/cvcomputer/</a> - high school computer club</li>
  <li><a href="/edit.py">/edit.py</a> - widgets test page</li>
  <li><a href="/easycrt/">/easycrt/</a> - EasyCRT pascal graphics library</li>
  <li><a href="/horde/">/horde/</a> - web mail (<a href="http://horde.org/imp/">IMP</a> 4.0)</li>
  <li><a href="/rref/">/rref/</a> - rvalue references for G++</li>
  <li><a href="/ssh/ssh.html">/ssh/</a> - ssh applet (<a href="http://javassh.org/">JTA</a> 2.0)</li>
  <li><a href="/twofish/twofish.html">/twofish/</a> - javascript encryption utility (MD5, twofish)</li>
  <li><a href="/viewcvs/">/viewcvs/</a> - ViewCVS for Windows</li>
  <li><a href="/viewvc.py">/viewvc.py</a> - repository browser (<a href="http://viewvc.org/">ViewVC</a> 1.0)</li>
  <li><a href="http://www.evilive.net/">www.evilive.net</a> - sister's home page</li>
</ul>

<h3>Miscellany</h3>
<ul>
  <li><a href="https://www.rapidvps.com/">RapidVPS</a> - site host</li>
</ul>
[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
