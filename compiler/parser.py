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
        self.iterator   = self.return_iterator()

    def parse(self):
        self.get_token()
        print self.curr_token[0]
        self.expect_token('TK_IDENTIFIER')



    #----------------------------------------
    #          PARSER HELPER METHODS                 
    #----------------------------------------

    def return_iterator(self):
        # Returns an iterator for tokens
        tokens = iter(self.tokens)
        return tokens


    def get_token(self):
        # Returns next token in list
        self.curr_token = self.iterator.next()
        return self.curr_token[0]

    def expect_token(self, token):
        # Checks if expected token is proper
        if self.curr_token[0] == token:
            return 
        else:
            self.error(token)

    def error(self, token):
        # Returns error message
        print "ERROR, expected token: %s but got %s." % (token, self.curr_token[0])

    #----------------------------------------
    #          PARSER GRAMMAR METHODS                
    #----------------------------------------

    def level(self):
    # Function for first level of grammar
    # L -> E | E < E | E > E | E <= E | E >= E | E = E | E != E
        print "level"


    def expression(self):
    # Function for building expressions
    # E -> E + T | E - T | T | E or T | E xor T
        print "expression"

    def term(self):
    # Function for building terms
    # T -> T x F | F | T / F | T div F | T mod F | T and F 
        print "term"


    def factor(self):
    # Function for building factors
    # F -> LITERAL | VARIABLE | - F | + F | ( L ) | not F
        print "factor"

    def expression_prime(self):
    # Function for second level of Expressions
    # E' -> empty | + T
        print "expression_prime"

    def term_prime(self):
    # Function for second level of Terms
        print "term_prime"

    def goal(self):
    # Function for starting grammar
        self.expression()
        print "goal"



        

