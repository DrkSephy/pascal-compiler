# -*- emulator.py -*-     
# -*- MIT License (c) 2014 -*-
# -*- drksephy.github.io -*-

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




