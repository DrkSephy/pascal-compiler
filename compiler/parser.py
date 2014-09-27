# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#     TODO      
#----------------------------------------

# - [done] Consumes tokens one at a time
# - [    ] Needs grammar to handle arithmetic structures
# - [    ] Needs to handle if statements
# - [    ] Needs to handle while statements
# - [    ] Needs to handle for statements
# - [    ] Needs to handle if-then-else statements
# - [    ] Create functions to handle each token
# - [    ] Returns parse tree

class Parser(object):

    def __init__(self, tokens, curr_token, op):
        # Parameters:
        #   * tokens : list of tuples of tokens
        #       - tokens produced by scanner
        #   * curr_token : current token being processed
        #       - current token being read
        #   * op : current operation to handle
        #       - current operation to print to stack
        self.tokens     = tokens
        self.curr_token = curr_token
        self.op         = op

    def parse(self):
        pass


    #----------------------------------------
    #          TOKEN HELPER METHODS
    #----------------------------------------

    def token_begin(self, token):
        pass

    def token_break(self, token):
        pass

    def token_const(self, token):
        pass

    def token_do(self, token):
        pass

    def token_downto(self, token):
        pass

    def token_else(self, token):
        pass

    def token_end(self, token):
        pass

    def token_end_program(self, token):
        pass

    def token_for(self, token):
        pass

    def token_function(self, token):
        pass


