---
layout: post
title: Removing borders around links when using hyperref
---

By default, the hyperref package adds borders around links in the document. Adding the following lines to your preamble fixes this: 
    
{% highlight latex %}
\hypersetup{colorlinks,
 linkcolor=black,
 filecolor=black,
 urlcolor=black,
 citecolor=black
}
{% endhighlight %}

