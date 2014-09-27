# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#                  TODO      
#----------------------------------------

# - [done] Consumes tokens one at a time
# - [    ] Needs grammar to handle arithmetic structures
# - [    ] Needs to handle if statements
# - [    ] Needs to handle while statements
# - [    ] Needs to handle for statements
# - [    ] Needs to handle if-then-else statements
# - [    ] Create functions to handle each token
# - [    ] Returns parse tree

#----------------------------------------------
#           ARITHMETIC GRAMMER
#----------------------------------------------

#----------------------------------------------
#
#   G   -> E | EOF
#   E   -> T E'
#   E'  -> empty | + T (+) E' | - T (-) E'
#   T   -> fT'
#   T'  -> empty | x F (*) T' | / F (/) T'
#   F   -> Lit | id | - F(-) | + F | not F | (F)
#
#-----------------------------------------------

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
    #      KEYWORD TOKEN HELPER METHODS
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

    def token_boolean(self, token):
        pass

    #----------------------------------------
    #      OPERATOR TOKEN HELPER METHODS
    #----------------------------------------

    def token_plus(self, token):
        pass

    def token_minus(self, token):
        pass

    def token_mult(self, token):
        pass

    def token_div_float(self, token):
        pass

    def token_div(self, token):
        pass

    def token_mod(self, token):
        pass

    def token_colon(self, token):
        pass

    def token_equals(self, token):
        pass

    def token_assignment(self, token):
        pass

    def token_greater(self, token):
        pass

    def token_less(self, token):
        pass

    def token_greater_equals(self, token):
        pass

    def token_less_equals(self, token):
        pass

    def token_and(self, token):
        pass

    def token_or(self, token):
        pass

    def token_not(self, token):
        pass

    def token_semicolon(self, token):
        pass

    def token_open_parenthesis(self, token):
        pass

    def token_close_parenthesis(self, token):
        pass

    def token_quote(self, token):
        pass

    



