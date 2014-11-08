# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#                  TODO      
#----------------------------------------

# - [done] Consumes tokens one at a time
# - [done] Needs grammar to handle arithmetic structures
# - [done] Generate stack machine assembly
# - [    ] Print parse tree
# - [    ] Needs to handle if statements
# - [    ] Needs to handle while statements
# - [    ] Needs to handle for statements
# - [    ] Needs to handle if-then-else statements
# - [    ] Create functions to handle each token
# - [done] Returns parse tree

from prettytable import PrettyTable

class Parser(object):

    def __init__(self, tokens, curr_token, op, nodes = [], decorated_nodes = [], byte_array = [], 
                 symtable = [], lhs = '', rhs = ''):
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
        self.nodes              = nodes
        self.decorated_nodes    = decorated_nodes
        self.byte_array         = byte_array
        self.symtable           = symtable
        self.lhs                = lhs
        self.rhs                = rhs

    def parse(self):
        self.get_token()
        # self.expression()
        self.program()
        # self.goal()
        # return 
        # print self.decorated_nodes
        # print self.symtable
        return {'decorated_nodes' : self.decorated_nodes, 'symtable' : self.symtable}
        # return self.decorated_nodes


    #----------------------------------------
    #             PRETTY PRINTER             
    #----------------------------------------

    def printer(self, iterator, field_names, storage, data):
        # Returns: Ascii formatted table 
        #
        # Parameters:
        #   iterator: int
        #       token counter
        #   field_names: list of strings
        #       table headers
        #   storage: list
        #       row of data to append 
        #   data: list of dictionaries
        #      key, value pairs of metadata

        table = PrettyTable()
        table.field_names = field_names
        for datum in data:
            storage.append(iterator)
            storage.append(datum)
            table.add_row(storage)
            del storage[:]

            iterator += 1
        return table

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

    def program(self):
        # <program> ->
        #   <header>
        #   <declarations>
        #   <begin-statement>
        #   <halt>
        if self.curr_token[0] == 'TK_PROGRAM':
            print "Matched PROGRAM: " + self.curr_token[1]
            self.match('TK_PROGRAM')
            self.declarations()

    def declarations(self):
        # <declarations> ->
        #   <var decl>   ; <declarations>
        #   <label decl> ; <declarations>
        #   <prodecure>  ; <declarations>
        #   <function>   ; <declarations>
        self.var_decl()
        return 

    def var_decl(self):
        if self.curr_token[0] == 'TK_VAR':
            print "Matched TK_VAR: " + self.curr_token[1]
            self.match('TK_VAR')
        else:
            # Our next token isn't TK_VAR, so it must be begin 
            self.begin()
            return
        # Keep matching identifiers and commas
        while(1):
            if self.curr_token[0] == 'TK_IDENTIFIER':
                print "Matched TK_IDENTIFIER: " + self.curr_token[1]
                self.symtable.append({'NAME': self.curr_token[1], 'TYPE': 'empty', 'VALUE' : 0})
                self.match('TK_IDENTIFIER')
            if self.curr_token[0] == 'TK_COMMA': 
                print "Matched TK_COMMA: " + self.curr_token[1]
                self.match('TK_COMMA')
            if self.curr_token[0] == 'TK_COLON':
                print "Matched TK_COLON: " + self.curr_token[1]
                self.match('TK_COLON')
                break
        if self.curr_token[0] == 'TK_ID_INTEGER':
            print "Matched TK_ID_INTEGER: " + self.curr_token[1]
            # Now that we know the type of all the variables we declared
            # We go back and assign the types in our symbol table
            for vars in self.symtable:
                if vars['TYPE'] == 'empty':
                    vars['TYPE'] = 'integer'
            self.match('TK_ID_INTEGER')

        if self.curr_token[0] == 'TK_ID_REAL':
            print "Matched TK_ID_REAL: " + self.curr_token[1]
            # Now that we know the type of all the variables we declared
            # We go back and assign the types in our symbol table
            for vars in self.symtable:
                if vars['TYPE'] == 'empty':
                    vars['TYPE'] = 'real'
            self.match('TK_ID_REAL')


        if self.curr_token[0] == 'TK_SEMICOLON': 
            print "Matched TK_SEMICOLON: " + self.curr_token[1]
            self.match('TK_SEMICOLON')
        # Keep checking for declarations
        self.var_decl()


    def begin(self):
        # <begin-statement> ->
        #   begin <statements> end
        if self.curr_token[0] == 'TK_BEGIN':
            print "Matched TK_BEGIN: " + self.curr_token[1]
            self.match('TK_BEGIN')
        self.statements()
        return 
    
    def statements(self):
        # <statements> ->
        #   <while statement> ; <statement>
        #   <for statement>   ; <statement>
        #   <goto statement>  ; <statement>
        #   <if statement>    ; <statement>
        #   <case statement>  ; <statement>
        #   <assignment statement> ; <statement>
        #   <proc call>       ; <statement>
        while(1):
            if self.curr_token[0] == 'TK_IDENTIFIER':
                self.lhs = self.curr_token[1]
                print "Matched TK_IDENTIFIER: " + self.curr_token[1]
                self.match('TK_IDENTIFIER')

            if self.curr_token[0] == 'TK_ASSIGNMENT':
                print "Matched TK_ASSIGNMENT: " + self.curr_token[1]
                self.match('TK_ASSIGNMENT')
            # We've seen a variable and := (ex: x := )
            # Now we expect an expression
            self.expression()
            # Now that we have computed the RHS of the assignment
            # We need to update the symbol table
            # for var in self.symtable:
            #   if var['NAME'] == self.lhs:
            #        var['VALUE'] = self.rhs
            if self.curr_token[0] == 'TK_SEMICOLON':
                print "Matched TK_SEMICOLON: " + self.curr_token[1]
                self.match('TK_SEMICOLON')
                self.decorated_nodes.append({'instruction': 'pop ', 'value': self.lhs})

            if self.curr_token[0] == 'TK_END_CODE':
                break
        return

        
         
    def goal(self):
        # Goal -> Expression EOF
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
            print "Seen plus"
            self.match('TK_PLUS')
            self.term()
            self.postfix('TK_PLUS')
            self.expression_prime()
        elif self.curr_token[0] == 'TK_MINUS':
            self.match('TK_MINUS')
            self.term()
            self.postfix('TK_MINUS')
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
            self.postfix('TK_MULT')
            self.term_prime()
        elif self.curr_token[0] == 'TK_DIV_FLOAT':
            self.match('TK_DIV_FLOAT')
            self.factor()
            self.postfix('TK_DIV_FLOAT')
            self.term_prime()
        else:
            pass

    def factor(self):
        # Factor -> id

        if self.curr_token[0] == 'TK_IDENTIFIER':
            self.postfix(self.curr_token)
            self.match('TK_IDENTIFIER')

        if self.curr_token[0] == 'TK_INTEGER':
            self.postfix(self.curr_token)
            self.rhs = self.curr_token[1]
            self.match('TK_INTEGER')

    #----------------------------------------
    #        DECORATED GRAMMAR METHODS                
    #----------------------------------------

    def postfix(self, token):
        # Method for building postfix notation of tokens.

        if token[0] == 'TK_IDENTIFIER':
            self.decorated_nodes.append({'pop' : self.curr_token[1]})
        elif token[0] == 'TK_INTEGER':
            self.decorated_nodes.append({'instruction': 'push', 'value': self.curr_token[1]})
        elif token == 'TK_MULT':
            self.decorated_nodes.append({'instruction': 'mult', 'value': '*'})
        elif token == 'TK_PLUS':
            self.decorated_nodes.append({'instruction': 'add', 'value':  '+'})
        elif token == 'TK_MINUS':
            self.decorated_nodes.append({'instruction': 'minus', 'value':  '-'})
        else:
            pass

