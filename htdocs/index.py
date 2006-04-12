#!/usr/bin/env python
import web


class Page(web.BasePage):
  DATE = "$Date$"
  title = "Home"
  template = web.ezt(
"""[navbar]
<p>Hello, my name is Russell Yanofsky and this thing which you are looking at is my personal home page. It's always seemed to me that only the most boring, solipsistic, and ineffectual people write web pages about themselves. What other kinds of people could come up with the in-depth accounts of "my walk to the bus stop," the predictable rants about "people who talk on cell phones," the video/audio extravaganzas depicting "that time I went to the beach" that pervade the world wide web? And it always seems that the more elaborate these sites are and the richer in detail and scope, the more stupid and banal the person they describe. So really, it's surprising that I've made it this far in life without having a home page of my own. And because I'm who I am, it's pretty much inevitable now that I have this one that I'll be adding all sorts of features to it: An up to the minute blog and photojournal, free lifetime <tt>@yanofsky.org</tt> email accounts, weekly "funny caption" contests, free t-shirts, crossword puzzles, movie reviews, shopping discounts&mdash; And, I've already got an idea for a gangsta flash intro where I spit some mad rhymes, yo.</p>

<p>Which is all to say that I apologize for this site's existence. The fact is that I like reading people's homepages. Mostly because they provide a way of getting to know the strange creatures who inhabit internet mailing lists, newsgroups, and irc channels, who you may never meet in real life, but who might be up to interesting things when they are not involved in protracted arguments with you about the meaning of the <tt>foo</tt> parameter of the <tt>walla</tt> function in <tt>bar.c</tt>. Just in case anybody cares, I'm willing to engage in some navel gazing to provide this way for people to get to know me. And it is without further the apology that I present:</p>

<div class="head">The Facts of My Life</div>
<div class="subhead">A first person account, hereafter written in the third person so it might sound more impressive.</div>

<p>Russell Edward Yanofsky is a 24 year old, absolutely hopeless computer geek of the pale, skinny, awkward, shy, romantically inexperienced subtype whose characteristics he embodies to an extreme degree. Growing up in the (lower) upper-middle class suburbs of Central Pennsylvania, he had a happy, hopeful childhood as the oldest of three <a href="http://www.evilive.net/pages/family.htm">children</a>, raised by his mother and <a href="http://www.pneuro.com/practice/charles.html">father</a>. He excelled in his <a href="http://www.yeshivaacademy.org/">small, religious day school</a> and <a href="http://www.cvschools.org/high_school.cfm">large, public high school</a> with strong interests in math and science.</p>

<p>At the age of 18, he went to <a href="http://www.columbia.edu/">Columbia University</a> in New York City to study computer science, where he took a lot of interesting classes and met a lot of interesting people, living the laid-back college life. On the whole though, he was a little too laid-back, and ran aground academically in the last semester, failing two classes he needed for graduation. Which burned suddenly, and badly, making him think that what he really wanted to do then was something different, and that whatever it was should be the opposite of laid-back. So, somewhat improbably, instead of becoming a fifth year student, he enlisted in the <a href="http://www.benning.army.mil/infantry/">United States Army Infantry</a> where he completed basic training and a one year deployment to <a href="http://en.wikipedia.org/wiki/Baquba">Baquba, Iraq</a> with the "<a href="http://www.globalsecurity.org/military/agency/army/3id-3bde.htm">Sledgehammer Brigade</a>" of the 3rd Infantry Division (in <a href="http://blog.360.yahoo.com/blog-PLNtPtwzer9q.xZ7G38ARCNlGO3beXk">B Co 2/69</a>). He's still trying to sort out everything he saw and did in Iraq, but suffice it so say here that he thinks his experiences there were pretty much the same as those of the thousands of other soldiers he served with, and he thinks the whole thing has been portrayed pretty fairly in mainstream press coverage. He's not planning on going back to Iraq. He should be discharged from the Army in May 2006, and moving back to New York City to finish school and look for work.</p>

[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
