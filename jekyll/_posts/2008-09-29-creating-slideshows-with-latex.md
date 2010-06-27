---
layout: post
title: Creating slideshows with LaTeX
---

[LaTeX Beamer][1] is fantastic for this task. [This][2] page provides a good introduction to the package. Usually, to produce the actual slideshow, you wou would begin your document with something like the following: 
    
{% highlight latex %}
\documentclass{beamer}
\mode{
 \usetheme{Berlin}
 \usecolortheme{crane}
}
{% endhighlight %}

Of course, Berlin and crane can be changed to themes of your choice. A gallery of themes can be found [here][3], and examples of color themes can be found in section 17 (page 162 as of version 3.07) of the beamer manual. However, if you would like to print the slideshow as a handout (multiple slides on a single page), you can change the lines given above to: 
    
{% highlight latex %}
\documentclass[handout]{beamer}
\mode{
 \usetheme{default}
 \usecolortheme{seagull}
}
\usepackage{pgfpages}
\pgfpagesuselayout{4 on 1}[a4paper,landscape,border shrink=5mm]
{% endhighlight %}

And, if you would like to compress everything to an article format, use the following instead: 
    
{% highlight latex %}
\documentclass{article}
\usepackage{beamerarticle}
{% endhighlight %}

   [1]: http://latex-beamer.sourceforge.net/
   [2]: http://heather.cs.ucdavis.edu/~matloff/beamer.html
   [3]: http://mike.polycat.net/gallery/beamer-themes


