---
layout: post
title: Setting paper size and margins in LaTeX
---

Personally I dislike the large margins LaTeX defaults to. Adding the following line to the preamble allows you to adjust these (as well as setting the paper size): 
    
{% highlight latex %}
\usepackage[a4paper,left=2.25cm,right=2.25cm,top=2.5cm,bottom=2.5cm]{geometry}
{% endhighlight %}

