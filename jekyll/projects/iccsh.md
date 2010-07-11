---
layout: project-page
title: iCCsh
---

iCCsh is an interactive C Compiler shell. It allows C code to be quickly and
easily evaluated, without the need for manually constructing and compiling an
entire C source file. An example session is shown below:

{% highlight c %}
>>> int i
:declare i int i
>>> for(i = 0; i < 20; i++) \
...     printf("%d ", i); \
... printf("\n");
:eval for(i = 0; i < 20; i++) ...
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 
>>> :f hello
... void hello(const char *name) {
...     printf("Hello %s!\n", name);
... }
... 
>>> hello("world")
:eval hello("world")
Hello world!
>>> :i math
>>> %f cos(M_PI/4)
:printf %f cos(M_PI/4)
0.707107
{% endhighlight %}

iCCsh can also interface with native libraries, such as Xlib (X11):

{% highlight text %}
>>> :i X11/Xlib
>>> :l X11
>>> :d display Display *display
>>> display = XOpenDisplay("")
>>> :d screen Screen *screen
>>> screen = XScreenOfDisplay(display, 0)
>>> :p width=%d\nheight=%d\ndepth=%d \
...     screen->width, screen->height, screen->root_depth
width=1280
height=800
depth=24
>>> XCloseDisplay(display)
{% endhighlight %}

### Links

 - [Download][1]
 - Powered by [TinyCC][2]

 [1]: http://github.com/davidar/iccsh
 [2]: http://bellard.org/tcc/
