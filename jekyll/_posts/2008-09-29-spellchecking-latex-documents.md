---
layout: post
title: Spellchecking LaTeX documents
---

To spellcheck a LaTeX document, run the following command (replacing 'file.tex' with the name of your document): 
    
{% highlight bash %}
aspell -a -t < 'file.tex' | grep "&" | sort -u
{% endhighlight %}

