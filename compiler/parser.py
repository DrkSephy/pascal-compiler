# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#                  TODO      
#----------------------------------------

# - [done] Consumes tokens one at a time
# - [done] Needs grammar to handle arithmetic structures
# - [done] Generate stack machine assembly
# - [done] Handle repeat statements
# - [done] Handle if statements
# - [done] Handle while statements
# - [done] Handle for statements
# - [done] Handle if-then-else statements
# - [done] Create functions to handle each token
# - [done] Returns parse tree
# - [done] Create code array
# - [done] Create data array
# - [done] Create stack array
# - [done] Implement opcodes
# - [done] Create simulator 
# - [done] Build symbol tables
# - [    ] Implement Writeln( )
# - [    ] Implement Case statements
# - [    ] Implement Array operations

from prettytable import PrettyTable

class Parser(object):

    def __init__(self, tokens, curr_token, op = False, 
                 symtable = [], lhs = '', rhs = 0):
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
        self.instructions       = []
        self.symtable           = symtable
        self.lhs                = lhs
        self.rhs                = rhs
        self.address            = 0
        self.stack              = []
        self.ip                 = 0

    def parse(self):
        self.get_token()
        self.program()
        # print self.stack
        # print(self.printer(1, ['NUMBER', 'TYPE', 'NAME', 'VALUE', 'ADDRESS'], [], self.symtable))
        return {'decorated_nodes' : self.instructions, 'symtable' : self.symtable}

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
        # print 
        # Checks if expected token is proper
        if token == self.curr_token[0]:
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
        # print "Called program() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_PROGRAM':
            # print "Matched PROGRAM: " + self.curr_token[1]
            self.match('TK_PROGRAM')
            self.declarations()

    def declarations(self):
        # <declarations> ->
        #   <var decl>   ; <declarations>
        #   <label decl> ; <declarations>
        #   <prodecure>  ; <declarations>
        #   <function>   ; <declarations>
        # print "Called declarations() with " + self.curr_token[1]
        self.var_decl()
        return 

    def var_decl(self):
        # print "Called var_decl() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_VAR':
            # print "Matched TK_VAR: " + self.curr_token[1]
            self.match('TK_VAR')
        else:
            # Our next token isn't TK_VAR, so it must be begin 
            self.begin()
            return
        # Keep matching identifiers and commas
        while(1):
            if self.curr_token[0] == 'TK_IDENTIFIER':
                # print "Matched TK_IDENTIFIER: " + self.curr_token[1]
                self.symtable.append({'NAME': self.curr_token[1], 'TYPE': 'empty', 'VALUE' : 0, 'ADDRESS' : self.address})
                self.address += 4
                self.match('TK_IDENTIFIER')
            if self.curr_token[0] == 'TK_COMMA': 
                # print "Matched TK_COMMA: " + self.curr_token[1]
                self.match('TK_COMMA')
            if self.curr_token[0] == 'TK_COLON':
                # print "Matched TK_COLON: " + self.curr_token[1]
                self.match('TK_COLON')
                break

        if self.curr_token[0] == 'TK_ID_INTEGER':
            # print "Matched TK_ID_INTEGER: " + self.curr_token[1]
            # Now that we know the type of all the variables we declared
            # We go back and assign the types in our symbol table
            for vars in self.symtable:
                if vars['TYPE'] == 'empty':
                    vars['TYPE'] = 'integer'
            self.match('TK_ID_INTEGER')

        if self.curr_token[0] == 'TK_ID_REAL':
            # print "Matched TK_ID_REAL: " + self.curr_token[1]
            # Now that we know the type of all the variables we declared
            # We go back and assign the types in our symbol table
            for vars in self.symtable:
                if vars['TYPE'] == 'empty':
                    vars['TYPE'] = 'real'
            self.match('TK_ID_REAL')


        if self.curr_token[0] == 'TK_SEMICOLON': 
            # print "Matched TK_SEMICOLON: " + self.curr_token[1]
            self.match('TK_SEMICOLON')
        # Keep checking for declarations
        self.var_decl()


    def begin(self):
        # <begin-statement> ->
        #   begin <statements> end
        # print "Called begin() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_BEGIN':
            self.match('TK_BEGIN')
            while self.curr_token[0] != 'TK_END_CODE':
                self.statements()
            if self.curr_token[0] == 'TK_END_CODE':
                print "Reached end of program!" 
                self.instructions.append({'instruction': 'op_halt', 'ip': self.ip, 'value': 'END.'})
    
    def statements(self):
        # <statements> ->
        #   <while statement> ; <statement>
        #   <for statement>   ; <statement>
        #   <goto statement>  ; <statement>
        #   <repeat statement>; <statement>
        #   <if statement>    ; <statement>
        #   <case statement>  ; <statement>
        #   <assignment statement> ; <statement>
        #   <proc call>       ; <statement>
        # print "Called statements() with " + self.curr_token[1]
        while(1):
            if self.curr_token[0] == 'TK_REPEAT':
                self.repeat()
            elif self.curr_token[0] == 'TK_WHILE':
                self.while_loop() 
            elif self.curr_token[0] == 'TK_IF':
                self.if_statement()
            elif self.curr_token[0] == 'TK_FOR':
                self.for_statement()
            elif self.curr_token[0] == 'TK_WRITELN':
                self.writeln()
            elif self.curr_token[0] == 'TK_IDENTIFIER':
                self.lhs = self.curr_token[1]
                self.match('TK_IDENTIFIER')

            if self.curr_token[0] == 'TK_ASSIGNMENT':
                self.match('TK_ASSIGNMENT')
                self.op = True

            # We've seen a variable and := (ex: x := )
            # Now we expect an expression
            self.logic()
            if self.curr_token[0] == 'TK_SEMICOLON':
                self.match('TK_SEMICOLON')
                if self.op: 
                    self.instructions.append({'instruction': 'op_pop', 'ip': self.ip, 'value': self.lhs})
                    self.ip += 1
                    self.op = False

            if self.curr_token[0] == 'TK_END_CODE':
                break

            if self.curr_token[0] == 'TK_UNTIL':
                print "Seen TK_UNTIL"
                return

            if self.curr_token[0] == 'TK_ELSE':
                return

            if self.curr_token[0] == 'TK_TO':
                return
        return

    def for_statement(self):
        self.match('TK_FOR')
        self.statements()
        # Store the variable we need to increment
        loop_var = self.symtable[0]['NAME']
        self.match('TK_TO')
        loop_start = self.ip
        self.instructions.append({'instruction': 'op_push', 'ip': self.ip, 'value': loop_var, 'token': 'TK_IDENTIFIER' })
        self.ip += 1 
        self.factor()
        self.match('TK_DO')
        self.instructions.append({'instruction': 'op_greater', 'ip': self.ip, 'value': 'greater' })
        self.ip += 1 
        hole = self.ip
        self.instructions.append({'instruction': 'op_jtrue', 'ip': self.ip, 'value': hole })
        self.ip += 1 
        self.statements()

        # Increment loop var by 1 and go back to the start of execution
        self.instructions.append({'instruction': 'op_push', 'ip': self.ip, 'value': loop_var, 'token': 'TK_IDENTIFIER' })
        self.ip += 1 
        self.instructions.append({'instruction': 'op_push', 'ip': self.ip, 'value': 1, 'token': 'TK_INTEGER' })
        self.ip += 1 
        self.instructions.append({'instruction': 'op_add', 'ip': self.ip, 'value': '+' })
        self.ip += 1
        self.instructions.append({'instruction': 'op_pop', 'ip': self.ip, 'value': loop_var, 'token': 'TK_IDENTIFIER' })
        self.ip += 1 
        self.instructions.append({'instruction': 'op_jmp', 'ip': self.ip, 'value': loop_start })
        self.ip += 1 
        self.patch(hole)


    def writeln(self):
        self.match('TK_WRITELN')
        self.match('TK_OPEN_PARENTHESIS')
        self.logic()
        self.match('TK_CLOSE_PARENTHESIS')
        self.match('TK_SEMICOLON')
        self.instructions.append({'instruction': 'op_writeln', 'ip': self.ip, 'value': ''})
        self.ip += 1 

    def if_statement(self):
        # Handles the if statement
        self.match('TK_IF')
        self.logic()
        self.match('TK_THEN')
        # Mark instruction pointer if condition is true
        hole_1 = self.ip
        self.instructions.append({ 'instruction': 'op_jfalse', 'ip': self.ip, 'value': 0 })
        self.ip += 1 
        self.statements()

        # Handles the else statement
        if self.curr_token[0] == 'TK_ELSE':
            hole_2 = self.ip
            self.instructions.append({ 'instruction' : 'op_jmp', 'ip': self.ip, 'value': 0 })
            self.ip += 1 
            self.match('TK_ELSE')
            self.patch(hole_1)
            self.statements()
            self.patch(hole_2)

    def repeat(self): 
        self.match('TK_REPEAT')
        target = self.ip 
        self.statements()
        self.match('TK_UNTIL')
        self.logic()
        self.instructions.append({ 'instruction': 'op_jfalse', 'ip': self.ip, 'value': target })
        self.ip += 1 

    def patch(self, hole):
        self.instructions[hole]['value'] = self.ip  

    def while_loop(self):
        self.match('TK_WHILE')
        target = self.ip 
        self.logic()
        self.match('TK_DO')
        hole = self.ip
        self.instructions.append({ 'instruction': 'op_jfalse', 'ip': self.ip, 'value': target })
        self.ip += 1 
        self.statements()
        self.instructions.append({ 'instruction': 'op_jmp', 'ip': self.ip, 'value': target })
        self.ip += 1 
        self.patch(hole)
        return

    def logic(self):
        # Logic -> E | < E [<] E | > E [>] E | <= E [<=] E
        #           | >= E [>=] E | = E [=] E | != E [!=] E
        # print "Called logic() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_LESS':
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
        elif self.curr_token[0] == 'TK_NOT_EQUALS':
            self.match('TK_NOT_EQUALS')
            self.expression()
            self.postfix('TK_NOT_EQUALS')
        else:
            self.expression()

    def expression(self):
        # Expression -> Term Expression'
        # print "Called expression() with " + self.curr_token[1]
        self.term()
        self.expression_prime()

    def expression_prime(self):
        # Expression' -> + Term [+] Expression' | - Term [-] Expression' | e
        #                   | or T [or] E' | XOR T [xor] E' 
        # print "Called expression_prime() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_PLUS':
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
        # print "Called term() with " + self.curr_token[1]
        self.factor()
        self.term_prime()

    def term_prime(self):
        # Term' -> * Factor [*] Term' | / Factor [/] Term' | e 
        #               | MOD T [mod] F | AND T [and] F 

        # print "Called term_prime() with " + self.curr_token[1]
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
        elif self.curr_token[0] == 'TK_LESS':
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
        elif self.curr_token[0] == 'TK_NOT_EQUALS':
            self.match('TK_NOT_EQUALS')
            self.expression()
            self.postfix('TK_NOT_EQUALS')
        else:
            pass

    def factor(self):
        # Factor -> id | lit | not F | ( E ) | + F | - F
        # print "Called factor() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_IDENTIFIER':
            self.postfix(self.curr_token)
            self.match('TK_IDENTIFIER')
            return

        if self.curr_token[0] == 'TK_STRING':
            self.postfix(self.curr_token)
            self.match('TK_STRING')
            return

        if self.curr_token[0] == 'TK_INTEGER':
            self.postfix(self.curr_token)
            self.match('TK_INTEGER')
            return 

        if self.curr_token[0] == 'TK_NOT':
            self.match('TK_NOT')
            self.factor()
            self.postfix('TK_NOT')
            return

        if self.curr_token[0] == 'TK_OPEN_PARENTHESIS':
            self.match('TK_OPEN_PARENTHESIS')
            self.logic()
            self.match('TK_CLOSE_PARENTHESIS')
            return

    #----------------------------------------
    #        DECORATED GRAMMAR METHODS                
    #----------------------------------------

    def postfix(self, token):
        # Method for building postfix notation of tokens.
        if token[0] == 'TK_IDENTIFIER': 
            self.instructions.append({'instruction' : 'op_push', 'value': self.curr_token[1], 'ip': self.ip, 'token': self.curr_token[0]})
            self.ip += 1
        elif token[0] == 'TK_STRING':
            self.instructions.append({'instruction' : 'op_push', 'value': self.curr_token[1], 'ip': self.ip, 'token': self.curr_token[0]})
            self.ip += 1
        elif token[0] == 'TK_INTEGER':
            self.instructions.append({'instruction': 'op_push', 'value': self.curr_token[1], 'ip': self.ip, 'token': self.curr_token[0]})
            self.ip += 1
        elif token == 'TK_MULT':
            self.instructions.append({'instruction': 'op_mult', 'value': '*', 'ip': self.ip, 'token': '*'})
            self.ip += 1
        elif token == 'TK_DIV_FLOAT':
            self.instructions.append({'instruction': 'op_div_float', 'value': '/', 'ip': self.ip,  'token': '/'})
            self.ip += 1
        elif token == 'TK_PLUS':
            self.instructions.append({'instruction': 'op_add', 'value':  '+', 'ip': self.ip, 'token': '+'})
            self.ip += 1
        elif token == 'TK_MINUS':
            self.instructions.append({'instruction': 'op_minus', 'value':  '-', 'ip': self.ip, 'token': '-'})
            self.ip += 1
        elif token == 'TK_MOD':
            self.instructions.append({'instruction': 'op_mod', 'value': 'mod', 'ip': self.ip, 'token': 'TK_MOD'})
            self.ip += 1
        elif token == 'TK_OR':
            self.instructions.append({'instruction': 'op_or', 'value': 'or', 'ip': self.ip, 'token': 'TK_OR'})
            self.ip += 1
        elif token == 'TK_XOR':
            self.instructions.append({'instruction': 'op_xor', 'value': 'xor', 'ip': self.ip, 'token': 'TK_XOR'})
            self.ip += 1
        elif token == 'TK_AND':
            self.instructions.append({'instruction': 'op_and', 'value': 'and', 'ip': self.ip, 'token': 'TK_AND'})
            self.ip += 1
        elif token == 'TK_NOT':
            self.instructions.append({'instruction': 'op_not', 'value': 'not', 'ip': self.ip, 'token': 'TK_NOT'})
            self.ip += 1
        elif token == 'TK_LESS':
            self.instructions.append({'instruction': 'op_less', 'value': 'less', 'ip': self.ip, 'token': 'TK_LESS'})
            self.ip += 1
        elif token == 'TK_GREATER':
            self.instructions.append({'instruction': 'op_greater', 'value': 'greater', 'ip': self.ip, 'token': 'TK_GREATER'})
            self.ip += 1
        elif token == 'TK_LESS_EQUALS':
            self.instructions.append({'instruction': 'op_less_equals', 'value': 'less_equals', 'ip': self.ip, 'token': 'TK_LESS_EQUALS'})
        elif token == 'TK_GREATER_EQUALS':
            self.instructions.append({'instruction': 'op_greater_equals', 'value': 'greater_equals', 'ip': self.ip,  'token': 'TK_GREATER_EQUALS'})
            self.ip += 1
        elif token == 'TK_EQUALS':
            self.instructions.append({'instruction': 'op_equals', 'value': 'equals', 'ip': self.ip, 'token': 'TK_EQUALS'})
            self.ip += 1
        elif token == 'TK_NOT_EQUALS':
            self.instructions.append({'instruction': 'op_not_equals', 'value': 'not_equals', 'ip': self.ip, 'token': 'TK_NOT_EQUALS'})
            self.ip += 1
        else:
            pass


    #----------------------------------------
    #         SYM TABLE PRETTY PRINTER             
    #----------------------------------------
    def printer(self, iterator, field_names, storage, data):
        table = PrettyTable()
        table.field_names = field_names
        for datum in data: 
            storage.append(iterator)
            for k, v in datum.items():
                if str(k) == 'NAME':
                    storage.append(v)
                if str(k) == 'VALUE':
                    storage.append(v)
                if str(k) == 'TYPE':
                    storage.append(v)
                if str(k) == 'ADDRESS':
                    storage.append(hex(v))
            table.add_row(storage)
            del storage[:]
            iterator += 1
        return table

    #--------------------------
    #       HELPER METHODS
    #--------------------------
    def type(self, value):
        return type(value)



