---
layout: post
title: Converting images to grayscale in Linux with ImageMagick
---

To convert a single image 'image.jpg' to a grayscale version 'image-bw.jpg': 
    
{% highlight bash %}
convert image.jpg -colorspace Gray image-bw.jpg
{% endhighlight %}

To convert an entire directory in images to grayscale: 
    
{% highlight bash %}
mkdir bw && for i in *.jpg; do convert $i -colorspace Gray bw/$i; done
{% endhighlight %}

The grayscale images will be placed in a subdirectory named 'bw'. To convert something other than JPEGs, just change *.jpg to the appropriate file extension. For more information, see [here][1].

   [1]: http://imagemagick.org/Usage/color/#grayscale


