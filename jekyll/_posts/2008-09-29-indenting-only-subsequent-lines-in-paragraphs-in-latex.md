---
layout: post
title: Indenting only subsequent lines in paragraphs in LaTeX
---

In order to remove the indent at the beginning of paragraphs, and indent subsequent lines if present, add the following to your preamble: 
    
{% highlight latex %}
\newcommand{\hangpara}{
 \setlength{\parindent}{0cm} % don't indent new paragraphs
 \hangindent=0.7cm % indent all subsequent lines
}
{% endhighlight %}

Then add \hangpara before each new paragraph, for example: 
    
{% highlight latex %}
\hangpara
The quick brown fox jumps over the lazy dog.

\hangpara
The quick brown fox jumps over the lazy dog again.
{% endhighlight %}

