---
layout: post
title: Command-line scanning
---

First you need to find the ID of the required device: 
    
{% highlight bash %}
scanimage -L
{% endhighlight %}

Output: 

    device `v4l:/dev/video0' is a Noname Acer CrystalEye webcam virtual device
    device `net:linux-box.local:hpaio:/usb/Photosmart_C4100_series?serial=XXXXXXXXXXXXXX' is a Hewlett-Packard Photosmart_C4100_series all-in-one

In this case the device ID is net:linux-box.local:hpaio:/usb/Photosmart_C4100_series?serial=XXXXXXXXXXXXXX Then, for colour scanning: 
    
{% highlight bash %}
scanimage -d "net:linux-box.local:hpaio:/usb/Photosmart_C4100_series?serial=XXXXXXXXXXXXXX" \
--mode Color --resolution 300dpi | pnmtopng - > image.png
{% endhighlight %}

Or for greyscale scanning: 
    
{% highlight bash %}
scanimage -d "net:linux-box.local:hpaio:/usb/Photosmart_C4100_series?serial=XXXXXXXXXXXXXX" \
--mode Gray --resolution 300dpi | pnmtopng - > image.png
{% endhighlight %}

