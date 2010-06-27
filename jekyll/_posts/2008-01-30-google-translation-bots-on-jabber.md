---
layout: post
title: Google Translation Bots on Jabber
---

This isn't exactly current news, but I only just recently got around to checking it out :) . A little while back Google released some [GTalk translation bots][1], which are a lot more handy for quickly translating text than having to go through the web interface. However, it seems they are only available through GTalk, and not to the general Jabber public (at least when I tried). I have a GTalk account, but prefer to do things through my Jabber.org account. Luckily, there's a [Jabber-Jabber transport (J2J)][2] over at JRuDevels.org. Essentially you just register at the gtalk.jrudevels.org service through your Jabber client (personally I like [Psi][3]), enter your GTalk username and password where appropriate, and gmail.com in the 'server' field (unless your ID ends with something other than @gmail.com). Here's a list of the currently available bots you can now add (using the [Jabber Roster Utility][4]): 
    
{% highlight diff %}
+,en2fr%bot.talk.google.com@gtalk.jrudevels.org,English-French,to,Translation Bots
+,en2es%bot.talk.google.com@gtalk.jrudevels.org,English-Spanish,to,Translation Bots
+,en2el%bot.talk.google.com@gtalk.jrudevels.org,English-Greek,to,Translation Bots
+,en2de%bot.talk.google.com@gtalk.jrudevels.org,English-German,to,Translation Bots
+,en2ar%bot.talk.google.com@gtalk.jrudevels.org,English-Arabic,to,Translation Bots
+,el2en%bot.talk.google.com@gtalk.jrudevels.org,Greek-English,to,Translation Bots
+,de2fr%bot.talk.google.com@gtalk.jrudevels.org,German-French,to,Translation Bots
+,de2en%bot.talk.google.com@gtalk.jrudevels.org,German-English,to,Translation Bots
+,ar2en%bot.talk.google.com@gtalk.jrudevels.org,Arabic-English,to,Translation Bots
+,en2ja%bot.talk.google.com@gtalk.jrudevels.org,English-Japanese,to,Translation Bots
+,zh2en%bot.talk.google.com@gtalk.jrudevels.org,Chinese-English,to,Translation Bots
+,ru2en%bot.talk.google.com@gtalk.jrudevels.org,Russian-English,to,Translation Bots
+,nl2en%bot.talk.google.com@gtalk.jrudevels.org,Dutch-English,to,Translation Bots
+,ko2en%bot.talk.google.com@gtalk.jrudevels.org,Korean-English,to,Translation Bots
+,ja2en%bot.talk.google.com@gtalk.jrudevels.org,Japanese-English,to,Translation Bots
+,it2en%bot.talk.google.com@gtalk.jrudevels.org,Italian-English,to,Translation Bots
+,fr2en%bot.talk.google.com@gtalk.jrudevels.org,French-English,to,Translation Bots
+,fr2de%bot.talk.google.com@gtalk.jrudevels.org,French-German,to,Translation Bots
+,es2en%bot.talk.google.com@gtalk.jrudevels.org,Spanish-English,to,Translation Bots
+,en2zh%bot.talk.google.com@gtalk.jrudevels.org,English-Chinese,to,Translation Bots
+,en2ru%bot.talk.google.com@gtalk.jrudevels.org,English-Russian,to,Translation Bots
+,en2nl%bot.talk.google.com@gtalk.jrudevels.org,English-Dutch,to,Translation Bots
+,en2ko%bot.talk.google.com@gtalk.jrudevels.org,English-Korean,to,Translation Bots
+,en2it%bot.talk.google.com@gtalk.jrudevels.org,English-Italian,to,Translation Bots
{% endhighlight %}
    

(these will get added to a group named 'Translation Bots')

   [1]: http://googletalk.blogspot.com/2007/12/merry-christmas-god-jul-and.html
   [2]: http://wiki.jrudevels.org/Eng:J2J
   [3]: http://psi-im.org/
   [4]: https://beta.unclassified.de/projekte/jru-php/jru.php


