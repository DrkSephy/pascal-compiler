pascal-compiler
---------------

A Pascal compiler built using Python. 

Restrictions
------------

As a means to learn, no libraries will be used for heavy lifting of the implementation of the scanner, parser or abstract syntax tree. The only libraries being used within this project are:

* [Pretty Tables](https://github.com/dprince/python-prettytable) : Library for printing ascii tables, useful for formatting debug statements and generated tokens to console.

Compiler Research Links
-----------------------

* [Writing Compilers with llvm-py](http://www.slideshare.net/mdevan/llvmpy-w)
* [Pascal Keywords](http://wiki.freepascal.org/Reserved_words)
* [Pascal Operators](http://www.tutorialspoint.com/pascal/pascal_operators.htm)
* [Symbol Tables](http://en.wikipedia.org/wiki/Symbol_table)
* [System Functions](http://www.freepascal.org/docs-html/rtl/system/index-5.html)
* [Data Types](http://wiki.freepascal.org/Variables_and_Data_Types)
* [Parsers and Compilers](http://parsingintro.sourceforge.net/#contents_item_7)
* [How does an interpreter/compiler work?](http://forums.devshed.com/programming-languages-139/interpreter-compiler-312483.html#post1342279)
* [Top Down Recursive Parsing](https://www.cs.duke.edu/~raw/cps218/Handouts/TDRD.htm)

Compiling Pascal on Mac OS X
----------------------------

If you do not want to use an IDE to write and compile Pascal code, it is highly recommended to simply compile pascal programs
through the command line. To do so, follow these steps.

* Download 'fpc' (Free Pascal Compiler) [here](http://www.hu.freepascal.org/lazarus/). If running on an intel-based Mac, download and install`fpc-2.6.0.intel-macosx.dmg`, and if you are on a PowerPC Macbook, download and install `fpc-2.6.0.powerpc-macosx.dmg`.

This should be all you need. Given the following sample program, `hello.pas`:

    program HelloWorld;
    uses crt; 

    (* Here the main program block starts *)
    begin
        writeln('Hello World!');
    end.

You can compile `hello.pas` using `fpc hello.pas` on the command line, producing `hello.o` and `hello`. You can now execute the executable using `./hello`, printing `'Hello World!'`. 



LICENSE
-------

The MIT License (MIT)

Copyright (c) 2014 David Leonard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
