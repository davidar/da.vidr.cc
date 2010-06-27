---
layout: project-page
title: Stumble
---

Tools for interacting with StumbleUpon.

Stumble currently provides two interfaces to [StumbleUpon][1]: 

  * **Stumble:** command-line interface to StumbleUpon
  * **KStumble:** service-menu for using StumbleUpon with Konqueror

### Requirements

  * Perl, with: 

    * Digest::SHA1 - `sudo aptitude install libdigest-sha1-perl` on Ubuntu/Debian; `emerge Digest-SHA1` on Gentoo
    * LWP sudo aptitude install libwww-perl on Ubuntu/Debian

  * KDE 3.5.x or 4.0.0 (for KStumble)

**NB: If you have trouble extracting the 0.2 release, you may need to rename it from 'stumble-0.2.tar.gz' to 'stumble-0.2.tar'. Sorry about this.**

### Links

  * **[Downloads][2]**
  * **[Documentation][3]**
  * [Google Code Project Page][4]
  * [KDE-Apps.org Project Page][5]

In order to checkout the latest development code, do the following: 
    
{% highlight bash %}
svn co http://stumble.googlecode.com/svn/trunk/ stumble
{% endhighlight %}

### Press

  * [Free Your Media][6]

   [1]: http://www.stumbleupon.com/
   [2]: http://code.google.com/p/stumble/downloads/list
   [3]: http://code.google.com/p/stumble/w/list
   [4]: http://code.google.com/p/stumble/
   [5]: http://kde-apps.org/content/show.php?content=73237
   [6]: http://free-your-media.net/2008/01/19/stumbleupon-for-konqueror/


