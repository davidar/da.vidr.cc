---
layout: post
title: Batch resizing a directory of images in Linux with ImageMagick
---

To replace all JPEGs in a directory with resized versions: 
    
{% highlight bash %}
mogrify -resize 720x576 *.jpg
{% endhighlight %}

Note that this will retain the aspect ratio, such that the image is scaled so it will fit inside a box of the given dimensions. To force the image to be stretched to the given dimensions instead: 
    
{% highlight bash %}
mogrify -resize 720x576! *.jpg
{% endhighlight %}

[[novell.com]][1]

   [1]: http://www.novell.com/coolsolutions/tip/16524.html


