---
layout: post
title: Printing the 'therefore' symbol in LaTeX
---

The [AMS][1] packages provide this functionality (as well as many other things). Add the following lines to the preamble: 
    
{% highlight latex %}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
{% endhighlight %}

Then the therefore symbol can be used: 
    
{% highlight latex %}
$ ... \therefore ... $
{% endhighlight %}

   [1]: http://www.ams.org/tex/amslatex.html


