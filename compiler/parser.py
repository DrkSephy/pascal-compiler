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
                 symtable = [], lhs = '', rhs = '', address = 0):
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
        self.address            = address

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
                self.symtable.append({'NAME': self.curr_token[1], 'TYPE': 'empty', 'VALUE' : 0, 'ADDRESS' : self.address})
                self.address += 4
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
            self.logic()

            if self.curr_token[0] == 'TK_SEMICOLON':
                print "Matched TK_SEMICOLON: " + self.curr_token[1]
                self.match('TK_SEMICOLON')
                self.decorated_nodes.append({'instruction': 'pop', 'value': self.lhs})

            if self.curr_token[0] == 'TK_END_CODE':
                break
        return

        
         
    def goal(self):
        # Goal -> Expression EOF
        self.expression()
        if self.curr_token[0] == 'TK_EOF':
            return 

    def logic(self):
        # Logic -> E | < E [<] E | > E [>] E | <= E [<=] E
        #           | >= E [>=] E | = E [=] E
        if self.curr_token[0] == 'TK_LESS':
            print "hello"
            self.match('TK_LESS')
            self.expression()
            self.postfix('TK_LESS')
        elif self.curr_token[0] == 'TK_GREATER':
            self.match('TK_GREATER')
            self.expression()
            self.postfix('TK_GREATER')
        elif self.curr_token[0] == 'TK_LESS_EQUALS':
            self.match('TK_LESS_EQUALS')
            self.expression()
            self.postfix('TK_LESS_EQUALS')
        elif self.curr_token[0] == 'TK_GREATER_EQUALS':
            self.match('TK_GREATER_EQUALS')
            self.expression()
            self.postfix('TK_GREATER_EQUALS')
        elif self.curr_token[0] == 'TK_EQUALS':
            self.match('TK_EQUALS')
            self.expression()
            self.postfix('TK_EQUALS')
        else:
            self.expression()

    def expression(self):
        # Expression -> Term Expression'

        self.term()
        self.expression_prime()

    def expression_prime(self):
        # Expression' -> + Term [+] Expression' | - Term [-] Expression' | e
        #                   | or T [or] E' | XOR T [xor] E' 

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
        elif self.curr_token[0] == 'TK_OR':
            self.match('TK_OR')
            self.term()
            self.postfix('TK_OR')
            self.expression_prime()
        elif self.curr_token[0] == 'TK_XOR':
            self.match('TK_XOR')
            self.term()
            self.postfix('TK_XOR')
            self.expression_prime()
        else:
            pass

    def term(self):
        # Term -> Factor Term'

        self.factor()
        self.term_prime()

    def term_prime(self):
        # Term' -> * Factor [*] Term' | / Factor [/] Term' | e 
        #               | MOD T [mod] F | AND T [and] F 

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
        elif self.curr_token[0] == 'TK_MOD':
            self.match('TK_MOD')
            self.factor()
            self.postfix('TK_MOD')
            self.term_prime()
        elif self.curr_token[0] == 'TK_AND': 
            self.match('TK_AND')
            self.factor()
            self.postfix('TK_AND')
            self.term_prime()
        else:
            pass

    def factor(self):
        # Factor -> id | lit | not F

        if self.curr_token[0] == 'TK_IDENTIFIER':
            self.postfix(self.curr_token)
            self.match('TK_IDENTIFIER')

        if self.curr_token[0] == 'TK_INTEGER':
            self.postfix(self.curr_token)
            self.match('TK_INTEGER')

        if self.curr_token[0] == 'TK_NOT':
            self.match('TK_NOT')
            self.factor()
            self.postfix('TK_NOT')

    #----------------------------------------
    #        DECORATED GRAMMAR METHODS                
    #----------------------------------------

    def postfix(self, token):
        # Method for building postfix notation of tokens.

        if token[0] == 'TK_IDENTIFIER':
            self.decorated_nodes.append({'instruction' : 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
        elif token[0] == 'TK_INTEGER':
            self.decorated_nodes.append({'instruction': 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
        elif token == 'TK_MULT':
            self.decorated_nodes.append({'instruction': 'mult', 'value': '*', 'token': '*'})
        elif token == 'TK_DIV_FLOAT':
            self.decorated_nodes.append({'instruction': 'div_float', 'value': '/', 'token': '/'})
        elif token == 'TK_PLUS':
            self.decorated_nodes.append({'instruction': 'add', 'value':  '+', 'token': '+'})
        elif token == 'TK_MINUS':
            self.decorated_nodes.append({'instruction': 'minus', 'value':  '-', 'token': '-'})
        elif token == 'TK_MOD':
            self.decorated_nodes.append({'instruction': 'mod', 'value': 'mod', 'token': 'TK_MOD'})
        elif token == 'TK_OR':
            self.decorated_nodes.append({'instruction': 'or', 'value': 'or', 'token': 'TK_OR'})
        elif token == 'TK_XOR':
            self.decorated_nodes.append({'instruction': 'xor', 'value': 'xor', 'token': 'TK_XOR'})
        elif token == 'TK_AND':
            self.decorated_nodes.append({'instruction': 'and', 'value': 'and', 'token': 'TK_AND'})
        elif token == 'TK_NOT':
            self.decorated_nodes.append({'instruction': 'not', 'value': 'not', 'token': 'TK_NOT'})
        elif token == 'TK_LESS':
            self.decorated_nodes.append({'instruction': 'less', 'value': 'less', 'token': 'TK_LESS'})
        elif token == 'TK_GREATER':
            self.decorated_nodes.append({'instruction': 'greater', 'value': 'greater', 'token': 'TK_GREATER'})
        elif token == 'TK_LESS_EQUALS':
            self.decorated_nodes.append({'instruction': 'less_equals', 'value': 'less_equals', 'token': 'TK_LESS_EQUALS'})
        elif token == 'TK_GREATER_EQUALS':
            self.decorated_nodes.append({'instruction': 'greater_equals', 'value': 'greater_equals', 'token': 'TK_GREATER_EQUALS'})
        elif token == 'TK_EQUALS':
            self.decorated_nodes.append({'instruction': 'equals', 'value': 'equals', 'token': 'TK_EQUALS'})
        else:
            pass

