pascal-compiler
---------------

Repository for a pascal compiler built using Python. Other possible languages for implementing this compiler are listed below (but are not limited to):

* JavaScript
* Rust

Compiler Research Links
-----------------------

* [Writing Compilers with llvm-py](http://www.slideshare.net/mdevan/llvmpy-w)


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
