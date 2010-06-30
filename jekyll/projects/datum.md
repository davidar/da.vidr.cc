---
layout: project-page
title: Datum
---

Datum is a simple question answering system.

 - [Online interface][7]
 - [Source code][1]

Natural language parsing and
generation is achieved through the use of templates. Fact retrieval and
inference is performed by a [Datalog][2] implementation, which uses the
"execution of concurrent machines" approach as described [here][3]. The fact and
rule databases are backed by JDO, so should be compatible with any database
system supported by a JDO implementation e.g. [DataNucleus][4].

Datum depends on the following libraries:

 - [DataNucleus][4]
 - [ANTLR v3][5]
 - [Apache Commons Lang][6]

 [1]: http://github.com/davidar/datum
 [2]: http://en.wikipedia.org/wiki/Datalog
 [3]: http://www.cs.sunysb.edu/~warren/xsbbook/node15.html
 [4]: http://www.datanucleus.org/
 [5]: http://antlr.org/
 [6]: http://commons.apache.org/lang/
 [7]: http://j.da.vidr.cc/projects/datum/
