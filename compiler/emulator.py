# -*- emulator.py -*-     
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

# * Reads <target> program from command line.
# * Simply prints out the <target> program.

################
#    USAGE     #
################

# python emulator.py <target program>

################
#     TODO     #
################

# - [done] Read <target program>
# - [done] Print program 
# - [    ] Tokenize <target program>
# - [    ] Build Parser
# - [    ] Build Abstract Syntax Tree


import sys
import scanner
from scanner import Scanner


def usage():
    sys.stderr.write('Usage: Pascal filename\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    scanner = Scanner(1, 1, '', '', [], [])
    tokens = scanner.scan(filename)
    
    




