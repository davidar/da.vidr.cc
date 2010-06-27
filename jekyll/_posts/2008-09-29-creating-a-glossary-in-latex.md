---
layout: post
title: Creating a glossary in LaTeX
---

**Note that this uses the deprecated 'glossary' package. At the moment I'm using the 'nomencl' package, which LyX has built-in support for.**

First, add to your preamble something like this: 
    
{% highlight latex %}
\usepackage[style=list]{glossary} % can be obtained from http://www.ctan.org/tex-archive/macros/latex/contrib/glossary/
\makeglossary
\newacronym{GNU}{GNU's Not Unix}{description={A computer operating system composed entirely of free software.}}
\storeglosentry{linux}{name={Linux}, description={Any Unix-like computer operating system that uses the Linux kernel.}}
{% endhighlight %}

And add the following lines where you want the glossary to appear: 
    
{% highlight latex %}
\printglossary
\addcontentsline{toc}{chapter}{Glossary} % remove this line if you don't want a table of contents entry for the glossary
{% endhighlight %}

Then, where you want to reference glossary entries: 
    
{% highlight latex %}
\gls{linux} % displays name field of the linux entry (in this case "Linux")
\useGlosentry{linux}{GNU/Linux} % displays "GNU/Linux"
\GNU % displays "GNU's Not Unix (GNU)" the first time this is used
\GNU % displays "GNU" all subsequent times
% NB: remember to use \GNU\ if want to retain the space after the acronym
{% endhighlight %}

To generate the glossary, run: 
    
{% highlight bash %}
makeindex 'file.glo' -s 'file.ist' -t 'file.glg' -o 'file.gls' # replace 'file' with the appropriate name for your files
{% endhighlight %}

If you use [Kile][1], and want to generate the glossary from the menu, first do the following: 

  * Settings
  * Configure Kile...
  * Tools
  * Build
  * New Tool...
  * MakeGlossary
  * Next
  * MakeIndex
  * Finish
  * General
  * Command: makeindex
  * Options: '%S.glo' -s '%S.ist' -t '%S.glg' -o '%S.gls'
  * Advanced
  * Source extension: glo
  * Target extension: gls
  * Menu
  * Add tool to Build menu: Compile
  * OK

And then to generate the glossary do Build>Compile>MakeGlossary.

   [1]: http://kile.sourceforge.net/


