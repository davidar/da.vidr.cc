---
layout: project-page
title: LLJVM
---

LLJVM provides a set of tools and libraries for running comparatively low level languages (such as C) on the JVM.

The C to JVM bytecode compilation provided by LLJVM involves several steps. Source code is first compiled to [LLVM][2] intermediate representation (IR) by a frontend such as [llvm-gcc][13] or [clang][14]. LLVM IR is then translated to [Jasmin][3] assembly code, linked against other Java classes, and then assembled to JVM bytecode.

The use of LLVM IR as the intermediate representation allows more information about the source program to be preserved, compared to other methods which use MIPS binary as the intermediate representation. For example, functions are mapped to individual JVM methods, and all function calls are made with native JVM invocation instructions. This allows compiled code to be linked against arbitrary  Java classes, and Java programs to natively call individual functions in the compiled code. It also allows programs to be split across multiple classes (comparable to dynamic linking), rather than statically linking everything into a single class.

Also note that while C is currently the only supported input language, any language with a compiler targeting LLVM IR could potentially be supported.

There are several ways to obtain the current release:

 - For a quick demonstration of some pre-compiled classes, download the [runtime library][9] and the [demo package][10] to a directory on your machine, and run `java -jar lljvm-demo-0.2.jar`
 - To compile LLJVM from source, download the [source release][11], extract it, and follow the compilation instructions in the README file
 - If you have problems compiling from source and are running Linux on an i386-compatible platform, download the [binary release][12], extract it, and download the [runtime library][9] into the resulting directory, then follow the relevant usage instructions in the README file

#### Links

 - API Documentation - Java ([HTML][6]), Backend ([HTML][7], [PDF][8])
 - [Git repository][1]
 - [Google Code Project Page][5]
 - [Hacker News][4]
 - [LLVM][2]
 - [Jasmin][3]
 - [NestedVM][15]
 - [Cibyl][16]

 [1]: http://github.com/davidar/lljvm
 [2]: http://llvm.org/
 [3]: http://jasmin.sf.net/
 [4]: http://news.ycombinator.com/item?id=961834
 [5]: http://code.google.com/p/lljvm/
 [6]: http://static.da.vidr.cc/projects/lljvm/doc/java/index.html
 [7]: http://static.da.vidr.cc/projects/lljvm/doc/backend/classJVMWriter.html
 [8]: http://lljvm.googlecode.com/files/lljvm-doc-backend-0.2.pdf
 [9]: http://lljvm.googlecode.com/files/lljvm-0.2.jar
 [10]: http://lljvm.googlecode.com/files/lljvm-demo-0.2.jar
 [11]: http://lljvm.googlecode.com/files/lljvm-0.2.tar.gz
 [12]: http://lljvm.googlecode.com/files/lljvm-bin-linux-i386-0.2.tar.gz
 [13]: http://llvm.org/cmds/llvmgcc.html
 [14]: http://clang.llvm.org/
 [15]: http://nestedvm.ibex.org/
 [16]: http://code.google.com/p/cibyl/
