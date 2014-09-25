# -*- emulator.py -*-     
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

# * Reads <target> program from command line.


################
#    USAGE     #
################

# python emulator.py <target program>

################
#     TODO     #
################

# - [done] Read <target program>
# - [done] Print program 
# - [done] Tokenize <target program>
# - [    ] Build Parser
# - [    ] Build Abstract Syntax Tree


import sys
from scanner import Scanner
from parser import Parser


def usage():
    sys.stderr.write('Usage: Pascal filename\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    scanner  = Scanner(1, 1, '', '', [], [], False, False, False, False)
    tokens   = scanner.scan(filename)
    parser   = Parser(tokens, 0)
    ast      = parser.parse()
    
    




