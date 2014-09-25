# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#################
#     TODO      #
#################

# - [done] Consumes tokens one at a time
# - [    ] Needs grammar to handle arithmetic structures
# - [    ] Needs to handle if statements
# - [    ] Needs to handle while statements
# - [    ] Needs to handle for statements
# - [    ] Needs to handle if-then-else statements
# - [    ] Returns parse tree

class Parser(object):

    def __init__(self, tokens, curr_token):
        self.tokens     = tokens
        self.curr_token = curr_token

    def parse(self):
        for token in self.tokens:
            print "Handling token: " + str(token)
