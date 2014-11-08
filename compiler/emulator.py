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
from simulator import Simulator 


def usage():
    sys.stderr.write('Usage: Pascal filename\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    # Initialize scanner
    scanner  = Scanner(1, 1, '', '', [], [], False, False, False, False)
    # Pass in file name, return list of tokens
    tokens   = scanner.scan(filename)
    tokens.append(('EOF', 0, 0, 0))
    # Initialize parser
    parser   = Parser(tokens, 0, '')
    # Return the AST using tokens
    ast      = parser.parse()
    # Initialize the simulator
    # simulator = Simulator(ast, [], [], 0)
    # Simulate the AST
    # simulation = simulator.simulate(ast)

    
    
    




