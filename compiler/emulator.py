# -*- emulator.py -*-     
# -*- MIT License (c) 2014 -*-
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

def usage():
    sys.stderr.write('Usage: Pascal filename\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    print text




