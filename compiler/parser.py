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
        # Parameters:
        #   * tokens : list of tuples of tokens
        #   * curr_token : current token being processed
        self.tokens     = tokens
        self.curr_token = curr_token

    def parse(self):
        pass
