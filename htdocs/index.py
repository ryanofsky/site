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
<div class="subhead">A first person account, hereafter written in the third person so it will sound more impressive.</div>

<p>Russell Edward Yanofsky is a 24 year old, absolutely hopeless computer geek of the pale, skinny, awkward, shy, romantically inexperienced subtype whose characteristics he embodies to an extreme degree. Growing up in the (lower) upper-middle class suburbs of Central Pennsylvania, he had a happy, hopeful childhood as the oldest of three <a href="http://www.evilive.net/pages/family.htm">children</a>, raised by his mother and <a href="http://www.pneuro.com/practice/charles.html">father</a>. He excelled in his <a href="http://www.yeshivaacademy.org/">small, jewish day school</a> and <a href="http://www.cvschools.org/high_school.cfm">large, public high school</a> with strong interests in math and science.</p>

<p>At the age of 18, he went to <a href="http://www.columbia.edu/">Columbia University</a> to study computer science, where for four years he did not excel, achieving middling academic performance while failing to seek out the experiences and personal contacts that could prepare him for a career and life after college. In his last year, a growing sense of anxiety about the future combined (oddly) with a long-cultivated sense of detachment and ennui, with bad results. He simply didn't do any of the things &mdash; job interviews, grad school applications, course work &mdash; he was supposed to. In his second to last term, for the first time, he failed a class. In the last term, he failed every class except one, which put him a few credits short of becoming a certified Computer Scientist.</p>

<p>Instead of becoming a fifth year student (even for a little while), he decided to throw himself in a meat grinder and see what would happen. Or rather, seeking a change of pace, a challenge, and an opportunity for personal development, he enlisted in the <a href="http://www.benning.army.mil/infantry/">United States Army Infantry</a> where he completed basic training and a one year deployment to <a href="http://en.wikipedia.org/wiki/Baquba">Baquba, Iraq</a> with <a href="http://blog.360.yahoo.com/blog-PLNtPtwzer9q.xZ7G38ARCNlGO3beXk-">Bayonet Co 2/69</a>, <a href="http://www.globalsecurity.org/military/agency/army/3id-3bde.htm">3rd Brigade, 3rd Infantry Division</a>. 
Not to sound too negative about that, though. His prevailing attitude about serving in the Army has been one of cautious enthusiasm. And no doubt that after he's through slapping his forehead and muttering obscenities, he'll think about his turn as a humvee driver and M-16 wielding infantryman with a warm nostalgia.</p>

<p>Future challenges and opportunities for personal development lie ahead. By May, he should be discharged from the army and moving back to New York City to finish school and look for work.</p>
[footer]""")


if __name__ == '__main__':
  web.handle_cgi(Page)
