# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

# * Pascal Parser
# * Consumes tokens one at a time, builds parse tree


class Parser(object):

    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        for token in self.tokens:
            print "Token Type: " + str(token[0])
