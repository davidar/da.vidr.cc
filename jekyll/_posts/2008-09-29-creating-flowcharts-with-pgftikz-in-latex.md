---
layout: post
title: Creating flowcharts with PGF/TikZ in LaTeX
---

First, add to your preamble: 
    
{% highlight latex %}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows}

% styles for flowcharts
\tikzstyle{decision} = [diamond, draw, text width=4.5em, text badly centered, node distance=3cm, inner sep=0pt]
\tikzstyle{block} = [rectangle, draw, text width=5em, text centered, rounded corners, minimum height=4em]
{% endhighlight %}

Then, create flowcharts with something like the following: 
    
{% highlight latex %}
\begin{figure}
 \begin{center}
  \begin{tikzpicture}[node distance=2.5cm, auto, >=stealth]
   % nodes
   \node[block] (a)                                     {A};
   \node[block] (b)  [right of=a]                       {B};
   \node[decision,text width=2.8cm]
                (c)  [right of=b, node distance=3.3cm]  {C?};
   \node[block] (d)  [right of=c, node distance=3.6cm]  {D};
   \node[block] (e)  [below of=a, node distance=4cm]    {E};
   \node[block] (f)  [right of=e]                       {F};
   \node[block] (g)  [right of=f]                       {G};
   \node[block] (h)  [right of=g]                       {H};
   
   % edges
   \draw[->] (a) -- (b);
   \draw[->] (b) -- (c);
   \draw[->] (c) -- node[above] {yes} (d);
   \draw[->] (c.north) to [out=170,in=45] node[above] {no} (b.north);
   \draw[->] (d.south) to [out=210,in=20] (e.north);
   \draw[->] (e) -- (f);
   \draw[->] (f) -- (g);
   \draw[->] (g) -- (h);
  \end{tikzpicture}
  \caption{Flowchart}
  \label{flowchart}
 \end{center}
\end{figure}
{% endhighlight %}

This will produce something like the following:

![Flowchart][1]

   [1]: http://i36.photobucket.com/albums/e36/nemti/blog/pgftikz-flowchart.png


