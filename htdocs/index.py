#!/usr/bin/env python
import web


class Page(web.BasePage):
  title = "Home"
  template = web.ezt(
"""[navbar]
<div class=notugly>
<p>Hello, my name is Russell Yanofsky and this thing which you are looking at is my personal home page. It's always seemed to me that only the most boring, solipsistic, and ineffectual people write web pages about themselves. What other kinds of people could come up with the in-depth accounts of "my walk to the bus stop", the predictable rants about "people who talk on cell phones," the visual/audio extravaganzas depicting "that time I went to the beach" that pervade the world wide web? And it always seems that the more elaborate these sites are, the richer in detail and scope, the more stupid and banal the person they describe. So really, it's suprising that I've made it this far in life without having a home page of my own. And because I'm who I am, it's pretty much inevitable now that I have this site that I'll be adding all sorts of features to it: An up to the minute blog and photojournal, free lifetime <tt>@russ.hn.org</tt> email accounts, weekly "funny caption" contests, free t-shirts, crossword puzzles, movie reviews, shopping discounts&mdash; And, I've already got an idea for a gangsta flash intro where I spit some mad rhymes, yo.</p>

<p>Which is all to say that I apologize for this site's existence. The fact is that I like reading people's homepages. Mostly because they provide a way of getting to know the strange creatures who inhabit internet mailing lists, newgroups, and irc channels, who you may never meet in real life, but who might be up to interesting things when they are not involved in protracted arguments with you about the meaning of the <tt>foo</tt> parameter of the <tt>walla</tt> function in <tt>bar.c</tt>. Just in case anybody cares, I'm willing to engage in some navel gazing to provide this way for people to get to know me. And it is without further the apology that I present:</p>

<div style="font-size: large; font-weight: bold; text-align: center">The Facts of My Life</div>
<div style="font-size: small; font-style: italic; text-align:center">A first person account, hereafter written in the third person tense so it will sound more impressive.</div>

<p>Russell Edward Yanofsky is a 24 year old, absolutely hopeless, computer geek of the pale, skinny, awkward, shy, romantically inexperienced, subtype whose charactersicts he embodies to an extreme degree. Raised in the (lower) upper-middle class suburbs of Central Pennsylvania, he had a happy, hopeful childhood, the oldest of three children, raised by his mother and father. He Excelled in his <a href="http://yeshivaacademy.org"">small, jewish day school</a> and <a href="http://cvschools.org/">large, public high school</a> with a strong interest in math and science.
</div>""")


if __name__ == '__main__':
  web.handle_cgi(Page)
