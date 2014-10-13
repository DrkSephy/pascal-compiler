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

    def __init__(self, tokens, curr_token, op, nodes):
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
        self.nodes      = []

    def parse(self):
        self.logic()



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

    def logic(self):
    # Function for grammar logic
    # L -> E | E < E | E > E | E <= E | E >= E | E = E | E != E
        self.get_token()
        self.expression()
        print "level"


    def expression(self):
    # Function for building expressions
    # E -> E + T | E - T | T | E or T | E xor T
        if self.curr_token[0] == 'TK_INTEGER':
            self.term() 

        
        print "expression"

    def term(self):
    # Function for building terms
    # T -> T x F | F | T / F | T div F | T mod F | T and F 
        if self.curr_token[0] == 'TK_INTEGER':
            self.term()
            self.factor()
        # Get next token
        self.get_token()
        if self.curr_token[0] == 'TK_MULT':
            self.nodes.append(self.curr_token[0])
        self.factor()
        return
        print "term"


    def factor(self):
    # Function for building factors
    # F -> LITERAL | VARIABLE | - F | + F | ( L ) | not F
        if self.curr_token[0] == 'TK_INTEGER':
            self.nodes.append(self.curr_token[0])
            return
        print "factor"
