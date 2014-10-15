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

    def __init__(self, tokens, curr_token, op, nodes, decorated_nodes):
        # Parameters:
        #   * tokens : list of tuples of tokens
        #       - tokens produced by scanner
        #   * curr_token : current token being processed
        #       - current token being read
        #   * op : current operation to handle
        #       - current operation to print to stack
        self.tokens             = tokens
        self.curr_token         = curr_token
        self.op                 = op
        self.iterator           = self.return_iterator()
        self.nodes              = []
        self.decorated_nodes    = decorated_nodes

    def parse(self):
        self.goal()
        print self.nodes
        print self.decorated_nodes

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
        return

    def match(self, token):
        # Checks if expected token is proper
        if token == self.curr_token[0]:
            # Append leaf nodes into list
            self.nodes.append(self.curr_token[1])
            # Generate stack machine ASM
            self.code_generation(self.curr_token)
            # Get next token
            self.get_token()
            return True
        else:
            self.error(token)

    def error(self, token):
        # Returns error message
        print "ERROR, expected token: %s but got %s." % (token, self.curr_token[0])

    #----------------------------------------
    #          PARSER GRAMMAR METHODS                
    #----------------------------------------

    def goal(self):
        # Goal -> Expression EOF

        self.get_token()
        self.expression()
        if self.curr_token[0] == 'TK_EOF':
            return 

    def expression(self):
        # Expression -> Term Expression'

        self.term()
        self.expression_prime()

    def expression_prime(self):
        # Expression' -> + Term [+] Expression' | - Term [-] Expression' | e

        if self.curr_token[0] == 'TK_PLUS':
            self.match('TK_PLUS')
            self.term()
            self.expression_prime()
        elif self.curr_token[0] == 'TK_MINUS':
            self.match('TK_MINUS')
            self.term()
            self.expression_prime()
        else:
            pass

    def term(self):
        # Term -> Factor Term'

        self.factor()
        self.term_prime()

    def term_prime(self):
        # Term' -> * Factor [*] Term' | / Factor [/] Term' | e

        if self.curr_token[0] == 'TK_MULT':
            self.match('TK_MULT')
            self.factor()
            self.term_prime()
        elif self.curr_token[0] == 'TK_DIV_FLOAT':
            self.match('TK_DIV_FLOAT')
            self.factor()
            self.term_prime()
        else:
            pass

    def factor(self):
        # Factor -> id
        print self.curr_token[1]
        if self.curr_token[0] == 'TK_IDENTIFIER':
            self.match('TK_IDENTIFIER')

    #----------------------------------------
    #        DECORATED GRAMMAR METHODS                
    #----------------------------------------

    def code_generation(self, token):
        if token[0] == 'TK_IDENTIFIER':
            self.decorated_nodes.append('push ' + self.curr_token[1])
        elif token[0] == 'TK_MULT':
            self.decorated_nodes.append('mul')
        elif token[0] == 'TK_PLUS':
            self.decorated_nodes.append('add')
        else:
            pass
