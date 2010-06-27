---
layout: post
title: Creating A1 posters with LaTeX
---

Firstly, after downloading and installing the [textpos][1] package, begin the document with: 
    
{% highlight latex %}
\documentclass{a0poster}
\usepackage[landscape,a1paper]{geometry}
\usepackage[absolute]{textpos}
\textblockorigin{0cm}{0cm}
{% endhighlight %}

Then, to position blocks of text on the page, use the textblock* environment, such as: 
    
{% highlight latex %}
\begin{textblock*}{270mm}(530mm,13mm) % 270mm wide, 530mm left of and 13mm below top-left corner of page
 \section*{Hello World}
 The quick brown fox jumps over the lazy dog.
\end{textblock*}
{% endhighlight %}

In order to aid in positioning textblocks, temporarily adding the following to your preamble may be helpful: 
    
{% highlight latex %}
\usepackage[colorgrid,texcoord]{eso-pic} % add a grid to the page
{% endhighlight %}

   [1]: http://purl.org/nxg/dist/textpos


