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

    def token_identifier(self, token):
        pass

    def token_if(self, token):
        pass

    def token_label(self, token):
        pass

    def token_program(self, token):
        pass

    def token_repeat(self, token):
        pass

    def token_string(self, token):
        pass

    def token_then(self, token):
        pass

    def token_to(self, token):
        pass

    def token_type(self, token):
        pass

    def token_var(self, token):
        pass

    def token_while(self, token):
        pass

    def token_integer(self, token):
        pass

    def token_real(self, token):
        pass

    def token_char(self, token):
        pass



