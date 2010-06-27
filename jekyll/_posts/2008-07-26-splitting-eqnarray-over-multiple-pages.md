---
layout: post
title: Splitting eqnarray Over Multiple Pages
---

To allow the eqnarray environment in LaTeX to split over pages, add the following command somewhere in your document: 
    
{% highlight latex %}
\allowdisplaybreaks
{% endhighlight %}

Alternatively, to only have this active for a single eqnarray, use something like the following: 
    
{% highlight latex %}
{
\allowdisplaybreaks
\begin{eqnarray}
...
\end{eqnarray}
}
{% endhighlight %}

(from [here][1])

   [1]: http://www.math.unizh.ch/?tex_pdf_pp#6014


