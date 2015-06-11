**DejaVa** compiles Java source code to JVM bytecode, then disassembles it to Jasmin assembly code.

Powered by:
- [JCI](https://commons.apache.org/proper/commons-jci/)
- [ECJ](https://www.eclipse.org/jdt/core/)
- [ClassFileAnalyzer](https://github.com/davidar/classfileanalyzer)

## Example

The following `HelloWorld` class

```java
public class HelloWorld {
    private class Foo {
        public void bar() {
            System.out.println("Hello world!");
        }
    }
    public static void main(String[] args) {
        HelloWorld helloWorld = new HelloWorld();
        Foo foo = helloWorld.new Foo();
        foo.bar();
    }
}
```

produces the following disassembly

### HelloWorld$Foo

```jasmin
; HelloWorld$Foo.j

.bytecode 50.0
.source HelloWorld.java
.class HelloWorld$Foo
.super java/lang/Object
.inner class private Foo inner HelloWorld$Foo outer HelloWorld

.field final synthetic this$0 LHelloWorld;

.method private <init>(LHelloWorld;)V
  .limit stack 2
  .limit locals 2
  .var 0 is this LHelloWorld$Foo; from Label0 to Label9
Label0:
;    private class Foo {
  .line 2
  0: aload_0
  1: aload_1
  2: putfield HelloWorld$Foo/this$0 LHelloWorld;
  5: aload_0
  6: invokespecial java/lang/Object/<init>()V
Label9:
  9: return
.end method

.method public bar()V
  .limit stack 2
  .limit locals 1
  .var 0 is this LHelloWorld$Foo; from Label0 to Label8
Label0:
;            System.out.println("Hello world!");
  .line 4
  0: getstatic java/lang/System/out Ljava/io/PrintStream;
  3: ldc "Hello world!"
  5: invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
Label8:
;        }
  .line 5
  8: return
.end method

.method synthetic <init>(LHelloWorld;LHelloWorld$Foo;)V
  .limit stack 2
  .limit locals 3
;    private class Foo {
  .line 2
  0: aload_0
  1: aload_1
  2: invokespecial HelloWorld$Foo/<init>(LHelloWorld;)V
  5: return
.end method
```

### HelloWorld

```jasmin
; HelloWorld.j

.bytecode 50.0
.source HelloWorld.java
.class public HelloWorld
.super java/lang/Object
.inner class private Foo inner HelloWorld$Foo outer HelloWorld

.method public <init>()V
  .limit stack 1
  .limit locals 1
  .var 0 is this LHelloWorld; from Label0 to Label4
Label0:
;public class HelloWorld {
  .line 1
  0: aload_0
  1: invokespecial java/lang/Object/<init>()V
Label4:
  4: return
.end method

.method public static main([Ljava/lang/String;)V
  .limit stack 4
  .limit locals 3
  .var 0 is args [Ljava/lang/String; from Label0 to Label27
  .var 1 is helloWorld LHelloWorld; from Label8 to Label27
  .var 2 is foo LHelloWorld$Foo; from Label23 to Label27
Label0:
;        HelloWorld helloWorld = new HelloWorld();
  .line 8
  0: new HelloWorld
  3: dup
  4: invokespecial HelloWorld/<init>()V
  7: astore_1
Label8:
;        Foo foo = helloWorld.new Foo();
  .line 9
  8: new HelloWorld$Foo
  11: dup
  12: aload_1
  13: dup
  14: invokevirtual java/lang/Object/getClass()Ljava/lang/Class;
  17: pop
  18: aconst_null
  19: invokespecial HelloWorld$Foo/<init>(LHelloWorld;LHelloWorld$Foo;)V
  22: astore_2
Label23:
;        foo.bar();
  .line 10
  23: aload_2
  24: invokevirtual HelloWorld$Foo/bar()V
Label27:
;    }
  .line 11
  27: return
.end method
```
