#!/usr/bin/env python
import web


class Page(web.BasePage):
  title = "Links"
  template = web.ezt(
"""[navbar]
<div class=notugly>

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
<a href="http://www.dictionary.com/">Dictionary</a>,
<a href="http://dictionary.oed.com/entrance.dtl">OED</a>,
<a href="http://www.columbia.edu/~rey4/classes.html">Classes</a>,
<a href="http://astalavista.box.sk/">astalavista</a> (turn off popups for this),
<a href="http://msdn.microsoft.com/workshop/author/dhtml/reference/objects.asp">DHTML Reference</a>
</p>

<h3>Pages and Sites on this Machine</h3>
<ul>
  <li><a href="http://cvs.russ.hn.org/viewcvs.asp/">cvs.russ.hn.org</a> - CVS Web</li>
  <li><a href="/cvcomputer/">/cvcomputer/</a> - Club I founded in high school</li>
  <li><a href="/jica/">/jica/</a> - java citrix client</li>
  <li><a href="/twofish/twofish.html">/twofish/</a> - javascript encryption utility (MD5, twofish)</li>
  <li><a href="/easycrt/">/easycrt/</a> - EasyCRT pascal graphics library</li>
  <li><a href="/cs1007/">/cs1007/</a>, <a href="/cs3156/">/cs3156/</a> - Web pages for classes</li>
  <li><a href="/reference/">/reference/</a> - cached copies of slow pages</li>
</ul>

<h3>Miscellany</h3>
<ul>
  <li><a href="http://www.godecookery.com/clipart/clart.htm">Medieval Woodcuts Clipart Collection</a> - site's graphics come from here</li>
  <li><a href="http://oracle.seas.columbia.edu/wces/">WCES</a></li>
</ul>
</div>""")


if __name__ == '__main__':
  web.handle_cgi(Page())
