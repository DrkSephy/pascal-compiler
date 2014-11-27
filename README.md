pascal-compiler
---------------

A Pascal compiler built using Python. 

Restrictions
------------

As a means to learn, no libraries will be used for heavy lifting of the implementation of the scanner, parser or abstract syntax tree. The only libraries being used within this project are:

* [Pretty Tables](https://github.com/dprince/python-prettytable) : Library for printing ascii tables, useful for formatting debug statements and generated tokens to console.

Progress
--------

The following is a list of features that have been implemented.

- [x] &lt;program&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;header&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;declarations&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;begin-statement&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;halt> 
- [x] &lt;declarations&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;var decl&gt;;&lt;declarations&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;label decl&gt;;&lt;declarations&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;procedure decl&gt;;&lt;declarations&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;function decl&gt;;&lt;declarations&gt;
- [x] &lt;begin-statement&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;begin&lt;statements&gt;end
- [x] &lt;statements&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;while statement&gt;;&lt;statement&gt;
- [ ] &nbsp;&nbsp;&nbsp;&nbsp;&lt;goto statement&gt;;&lt;statement&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;repeat statement&gt;;&lt;statement&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;for statement&gt;;&lt;statement&gt;
- [ ] &nbsp;&nbsp;&nbsp;&nbsp;&lt;if statement&gt;;&lt;statement&gt;
- [ ] &nbsp;&nbsp;&nbsp;&nbsp;&lt;case statement&gt;;&lt;statement&gt;
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;assignment&gt;
- [ ] &nbsp;&nbsp;&nbsp;&nbsp;&lt;proc call&gt;
- [x] &lt;var decl&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;var[&lt;namelist&gt;:&lt;type&gt;]*
- [x] &lt;assignment&gt; -->
- [x] &nbsp;&nbsp;&nbsp;&nbsp;&lt;LHS&gt; := &lt;RHS&gt;

- [x] L -> E | < E [<] E | > E [>] E | <= E [<=] E | >= E [>=] E | = E [=] E | != E [!=] E
- [x] E -> TE'
- [x] E' -> + T [+] E' | - T [-] E' | e | OR T [OR] E' | XOR T [XOR] E'
- [x] T -> FT'
- [x] T' -> x F [x] T' | /F [/] T' | e | DIV F [DIV] T' | MOD F [MOD] T'
- [ ] F -> id | lit | (E) | -F | + F | not F
- [x] Need to implement (E)
- [ ] Need to implement -F and +F

###Compiler Research Links

######General 

* [Pascal Keywords](http://wiki.freepascal.org/Reserved_words)
* [Pascal Operators](http://www.tutorialspoint.com/pascal/pascal_operators.htm)
* [Symbol Tables](http://en.wikipedia.org/wiki/Symbol_table)
* [System Functions](http://www.freepascal.org/docs-html/rtl/system/index-5.html)
* [Data Types](http://wiki.freepascal.org/Variables_and_Data_Types)

######Compiler Theory

* [Parsers and Compilers](http://parsingintro.sourceforge.net/#contents_item_7)
* [How does an interpreter/compiler work?](http://forums.devshed.com/programming-languages-139/interpreter-compiler-312483.html#post1342279)

######Parsing Methods and Grammar theory

* [More notes on Recursive Parsing](http://math.hws.edu/javanotes/c9/s5.html)
* [Top Down Recursive Parsing](https://www.cs.duke.edu/~raw/cps218/Handouts/TDRD.htm)
* [Recursive Descent Parser](http://en.wikipedia.org/wiki/Recursive_descent_parser)
* [Terminals and Non-terminals](http://en.wikipedia.org/wiki/Terminal_and_nonterminal_symbols)
* [Pascal Grammar](https://www.cs.utexas.edu/users/novak/grammar.html)
* [Pascal Complete Grammar](http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=0CC0QFjAC&url=http%3A%2F%2Fwww.cse.iitk.ac.in%2Fusers%2Facprasad%2Fgrammar.pdf&ei=GtoyVJW8GI-byASbyoD4Cg&usg=AFQjCNG_vQuq3Wmejnc6EkPCd8XAitCntQ&sig2=sO6dazNpRIviE1dGQ_CfkA&bvm=bv.76802529,d.aWw)

######Bytecode

* [Python Disassembly](http://lance-modis.eosdis.nasa.gov/cgi-bin/imagery/realtime.cgi)



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
