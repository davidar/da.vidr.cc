---
layout: post
title: Converting videos to 3GP in Ubuntu Intrepid 8.10 with FFmpeg
---

The default installation of FFmpeg in Ubuntu Intrepid 8.10 doesn't support conversion to 3GP. According to [this][1], installing ubuntu-restricted-extras should fix this, but that didn't work in my case. So, you may need to manually install the required packages: 
    
{% highlight bash %}
sudo aptitude install \
libavcodec-unstripped-51 \
libavdevice-unstripped-52 \
libavformat-unstripped-52 \
libavutil-unstripped-49 \
libpostproc-unstripped-51 \
libswscale-unstripped-0
{% endhighlight %}

Then, to convert a video, you can either go the command-line route: 
    
{% highlight bash %}
ffmpeg -i input.mpg \
-vcodec h263 -s qcif -r 15 -b 100k \
-acodec libfaac -ac 1 -ar 32000 -ab 64k \
output.3gp
{% endhighlight %}

Which will convert to input.mpg to output.3gp with: 

  * H.263 video codec
  * QCIF video resolution (176x144)
  * 15fps
  * 100 kb/s video bitrate
  * AAC audio codec (through libfaac)
  * 1 audio channel
  * 32000 Hz audio sampling frequency
  * 64 kb/s audio bitrate

Alternatively, if you prefer using a GUI, you can try [Mobile Media Converter][2] ([direct link to v.1.4.1 .deb][3]), which seems to work pretty well, and also supports downloading videos directly from YouTube.

   [1]: https://bugs.launchpad.net/medibuntu/+bug/291011/comments/1
   [2]: http://www.miksoft.net/mobileMediaConverter.htm
   [3]: http://www.miksoft.net/products/mmc_1.4.1_i386.deb


