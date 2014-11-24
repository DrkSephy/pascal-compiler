# -*- parser.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#                  TODO      
#----------------------------------------

# - [done] Consumes tokens one at a time
# - [done] Needs grammar to handle arithmetic structures
# - [done] Generate stack machine assembly
# - [    ] Handle repeat statements
# - [    ] Handle if statements
# - [    ] Handle while statements
# - [    ] Handle for statements
# - [    ] Handle if-then-else statements
# - [done] Create functions to handle each token
# - [done] Returns parse tree
# - [done] Create code array
# - [done] Create data array
# - [done] Create stack array
# - [done] Implement opcodes
# - [done] Create simulator 
# - [done] Build symbol tables

from prettytable import PrettyTable

class Parser(object):

    def __init__(self, tokens, curr_token, op = False, nodes = [], decorated_nodes = [], byte_array = [], 
                 symtable = [], lhs = '', rhs = '', address = 0, token_loop = [], loop = False, stack = [],
                 ip = 0):
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
        self.token_loop         = token_loop
        self.loop               = loop
        self.stack              = stack
        self.ip                 = ip

    def parse(self):
        self.get_token()
        self.program()
        print(self.printer(1, ['NUMBER', 'TYPE', 'NAME', 'VALUE', 'ADDRESS'], [], self.symtable))
        # return {'decorated_nodes' : self.decorated_nodes, 'symtable' : self.symtable}

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
        # print self.token_loop
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
            print "Matched TK_BEGIN: " + self.curr_token[1]
            self.match('TK_BEGIN')
        self.statements()
        return 
    
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

            if self.curr_token[0] == 'TK_WHILE':
                self.while_loop()

            if self.curr_token[0] == 'TK_FOR':
                self.for_loop()

            if self.curr_token[0] == 'TK_IDENTIFIER':
                self.lhs = self.curr_token[1]
                print "Matched TK_IDENTIFIER: " + self.curr_token[1]
                self.match('TK_IDENTIFIER')

            if self.curr_token[0] == 'TK_ASSIGNMENT':
                print "Matched TK_ASSIGNMENT: " + self.curr_token[1]
                self.match('TK_ASSIGNMENT')
                self.op = True

            # We've seen a variable and := (ex: x := )
            # Now we expect an expression
            self.logic()
            if self.curr_token[0] == 'TK_SEMICOLON':
                print "Matched TK_SEMICOLON: " + self.curr_token[1]
                self.match('TK_SEMICOLON')
                if self.op: 
                    self.token_loop.append({'instruction': 'pop', 'value': self.lhs})
                    self.decorated_nodes.append({'instruction': 'pop', 'value': self.lhs})
                    self.simulate({'instruction': 'pop', 'value': self.lhs})
                    self.op = False

            if self.curr_token[0] == 'TK_TO':
                print "Going back to for loop"
                self.for_loop()

            if self.curr_token[0] == 'TK_END_CODE':
                break

            if self.curr_token[0] == 'TK_UNTIL':
                return
        return

    def repeat(self): 
        self.match('TK_REPEAT')
        self.loop = True
        self.statements()
        self.match('TK_UNTIL')
        self.logic()
        for node in self.decorated_nodes:
            print str(node) + str(self.ip)
        return 

    def while_loop(self):
        self.match('TK_WHILE')
        self.loop = True
        self.logic()
        self.match('TK_DO')
        self.statements()
        # Remove first pop
        self.token_loop.pop(0)
        while self.stack[0] == True:
            self.stack.pop(0)
            for instruction in self.token_loop:
                self.simulate(instruction)
        self.loop = False
        return

    def for_loop(self):

        if self.curr_token[0] == 'TK_FOR':
            self.match('TK_FOR')
            self.logic()
        print "BLAH"
        if self.curr_token[0] == 'TK_TO':
            self.match('TK_TO')
            print "Matched TK_TO"
        return

    def goal(self):
        # Goal -> Expression EOF
        # print "Called goal() with " + self.curr_token[1]
        self.expression()
        if self.curr_token[0] == 'TK_EOF':
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
        print "Called term() with " + self.curr_token[1]
        self.factor()
        self.term_prime()

    def term_prime(self):
        # Term' -> * Factor [*] Term' | / Factor [/] Term' | e 
        #               | MOD T [mod] F | AND T [and] F 

        print "Called term_prime() with " + self.curr_token[1]
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
        print "Called factor() with " + self.curr_token[1]
        if self.curr_token[0] == 'TK_IDENTIFIER':
            self.postfix(self.curr_token)
            self.match('TK_IDENTIFIER')
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
            print "Calling logic() from within factor()"
            self.logic()
            self.match('TK_CLOSE_PARENTHESIS')
            return

    #--------------------------
    #         SIMULATOR
    #--------------------------
    
    def simulate(self, node):
        print node
        print self.ip
        if node['instruction'] == 'push':
            if node['token'] == 'TK_IDENTIFIER':
                self.pushi(node['value'])
            else:
                self.push(node['value'])
        if node['instruction'] == 'or':
            self.op_or()
        if node['instruction'] == 'and':
            self.op_and()
        if node['instruction'] == 'xor':
            self.op_xor()
        if node['instruction'] == 'not':
            self.op_not()
        if node['instruction'] == 'mod':
            self.mod()
        if node['instruction'] == 'less':
            self.op_less()
        if node['instruction'] == 'greater':
            self.op_greater()
        if node['instruction'] == 'less_equals':
            self.op_lesseq()
        if node['instruction'] == 'greater_equals':
            self.op_greatereq()
        if node['instruction'] == 'not_equals':
            self.op_noteq()
        if node['instruction'] == 'equals':
            self.op_equals()
        if node['instruction'] == 'div_float':
            self.div_float()
        if node['instruction'] == 'add':
            self.add()
        if node['instruction'] == 'pop':
            self.pop(node['value'])
        if node['instruction'] == 'minus':
            self.minus()
        if node['instruction'] == 'mult':
            self.mult()
        print self.stack

    #----------------------------------------
    #        DECORATED GRAMMAR METHODS                
    #----------------------------------------

    def postfix(self, token):
        # Method for building postfix notation of tokens.
        self.ip += 1
        if token[0] == 'TK_IDENTIFIER':
            if self.loop:
                self.token_loop.append({'instruction' : 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]}) 
            self.decorated_nodes.append({'instruction' : 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
            self.simulate({'instruction' : 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
        elif token[0] == 'TK_INTEGER':
            if self.loop:
                self.token_loop.append({'instruction': 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
            self.decorated_nodes.append({'instruction': 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
            self.simulate({'instruction': 'push', 'value': self.curr_token[1], 'token': self.curr_token[0]})
        elif token == 'TK_MULT':
            if self.loop:
                self.token_loop.append({'instruction': 'mult', 'value': '*', 'token': '*'})
            self.decorated_nodes.append({'instruction': 'mult', 'value': '*', 'token': '*'})
            self.simulate({'instruction': 'mult', 'value': '*', 'token': '*'})
        elif token == 'TK_DIV_FLOAT':
            if self.loop:
                self.token_loop.append({'instruction': 'div_float', 'value': '/', 'token': '/'})
            self.decorated_nodes.append({'instruction': 'div_float', 'value': '/', 'token': '/'})
            self.simulate({'instruction': 'div_float', 'value': '/', 'token': '/'})
        elif token == 'TK_PLUS':
            if self.loop:
                self.token_loop.append({'instruction': 'add', 'value':  '+', 'token': '+'})
            self.decorated_nodes.append({'instruction': 'add', 'value':  '+', 'token': '+'})
            self.simulate({'instruction': 'add', 'value':  '+', 'token': '+'})
        elif token == 'TK_MINUS':
            if self.loop:
                self.token_loop.append({'instruction': 'minus', 'value':  '-', 'token': '-'})
            self.decorated_nodes.append({'instruction': 'minus', 'value':  '-', 'token': '-'})
            self.simulate({'instruction': 'minus', 'value':  '-', 'token': '-'})
        elif token == 'TK_MOD':
            if self.loop:
                self.token_loop.append({'instruction': 'mod', 'value': 'mod', 'token': 'TK_MOD'})
            self.decorated_nodes.append({'instruction': 'mod', 'value': 'mod', 'token': 'TK_MOD'})
            self.simulate({'instruction': 'mod', 'value': 'mod', 'token': 'TK_MOD'})
        elif token == 'TK_OR':
            if self.loop:
                self.token_loop.append({'instruction': 'or', 'value': 'or', 'token': 'TK_OR'})
            self.decorated_nodes.append({'instruction': 'or', 'value': 'or', 'token': 'TK_OR'})
            self.simulate({'instruction': 'or', 'value': 'or', 'token': 'TK_OR'})
        elif token == 'TK_XOR':
            if self.loop:
                self.token_loop.append({'instruction': 'xor', 'value': 'xor', 'token': 'TK_XOR'})
            self.decorated_nodes.append({'instruction': 'xor', 'value': 'xor', 'token': 'TK_XOR'})
            self.simulate({'instruction': 'xor', 'value': 'xor', 'token': 'TK_XOR'})
        elif token == 'TK_AND':
            if self.loop:
                self.token_loop.append({'instruction': 'and', 'value': 'and', 'token': 'TK_AND'})
            self.decorated_nodes.append({'instruction': 'and', 'value': 'and', 'token': 'TK_AND'})
            self.simulate({'instruction': 'and', 'value': 'and', 'token': 'TK_AND'})
        elif token == 'TK_NOT':
            if self.loop:
                self.token_loop.append({'instruction': 'not', 'value': 'not', 'token': 'TK_NOT'})
            self.decorated_nodes.append({'instruction': 'not', 'value': 'not', 'token': 'TK_NOT'})
            self.simulate({'instruction': 'not', 'value': 'not', 'token': 'TK_NOT'})
        elif token == 'TK_LESS':
            if self.loop:
                self.token_loop.append({'instruction': 'less', 'value': 'less', 'token': 'TK_LESS'})
            self.decorated_nodes.append({'instruction': 'less', 'value': 'less', 'token': 'TK_LESS'})
            self.simulate({'instruction': 'less', 'value': 'less', 'token': 'TK_LESS'})
        elif token == 'TK_GREATER':
            if self.loop:
                self.token_loop.append({'instruction': 'greater', 'value': 'greater', 'token': 'TK_GREATER'})
            self.decorated_nodes.append({'instruction': 'greater', 'value': 'greater', 'token': 'TK_GREATER'})
            self.simulate({'instruction': 'greater', 'value': 'greater', 'token': 'TK_GREATER'})
        elif token == 'TK_LESS_EQUALS':
            if self.loop:
                self.token_loop.append({'instruction': 'less_equals', 'value': 'less_equals', 'token': 'TK_LESS_EQUALS'})
            self.decorated_nodes.append({'instruction': 'less_equals', 'value': 'less_equals', 'token': 'TK_LESS_EQUALS'})
            self.simulate({'instruction': 'less_equals', 'value': 'less_equals', 'token': 'TK_LESS_EQUALS'})
        elif token == 'TK_GREATER_EQUALS':
            if self.loop:
                self.token_loop.append({'instruction': 'greater_equals', 'value': 'greater_equals', 'token': 'TK_GREATER_EQUALS'})
            self.decorated_nodes.append({'instruction': 'greater_equals', 'value': 'greater_equals', 'token': 'TK_GREATER_EQUALS'})
            self.simulate({'instruction': 'greater_equals', 'value': 'greater_equals', 'token': 'TK_GREATER_EQUALS'})
        elif token == 'TK_EQUALS':
            if self.loop:
                self.token_loop.append({'instruction': 'equals', 'value': 'equals', 'token': 'TK_EQUALS'})
            self.decorated_nodes.append({'instruction': 'equals', 'value': 'equals', 'token': 'TK_EQUALS'})
            self.simulate({'instruction': 'equals', 'value': 'equals', 'token': 'TK_EQUALS'})
        elif token == 'TK_NOT_EQUALS':
            if self.loop:
                self.token_loop.append({'instruction': 'not_equals', 'value': 'not_equals', 'token': 'TK_NOT_EQUALS'})
            self.decorated_nodes.append({'instruction': 'not_equals', 'value': 'not_equals', 'token': 'TK_NOT_EQUALS'})
            self.simulate({'instruction': 'not_equals', 'value': 'not_equals', 'token': 'TK_NOT_EQUALS'})
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
    #         OP CODES
    #--------------------------

    def op_lesseq(self):
        val = int(self.stack[1]) <= int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_noteq(self):
        val = int(self.stack[1]) != int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_equals(self):
        val = int(self.stack[1]) == int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_greatereq(self):
        val = int(self.stack[1]) >= int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return


    def op_greater(self):
        val = int(self.stack[1]) > int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_less(self):
        val = int(self.stack[1]) < int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return 

    def op_not(self):
        val = not int(self.stack[0])
        self.stack.remove(self.stack[0])
        self.push(val)
        return 

    def op_and(self):
        val = int(self.stack[1]) and int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_xor(self):
        val = int(self.stack[1]) ^ int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def op_or(self):
        val = int(self.stack[1]) or int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def mod(self):
        val = int(self.stack[1]) % int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return 

    def div_float(self):
        val = int(self.stack[1]) / int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return 

    def pushi(self, value):
        for var in self.symtable:
            if var['NAME'] == value:
                self.stack.insert(0, var['VALUE'])
        return

    def push(self, value):
        self.stack.insert(0, value)
        return

    def pop(self, value):
        val = self.stack[0]
        self.stack.remove(self.stack[0])
        for var in self.symtable:
            if var['NAME'] == value:
                var['VALUE'] = val
        return

    def mult(self):
        val = int(self.stack[1]) * int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    def add(self):
        val = int(self.stack[1]) + int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return


    def minus(self):
        val = int(self.stack[1]) - int(self.stack[0])
        self.stack.remove(self.stack[1])
        self.stack.remove(self.stack[0])
        self.push(val)
        return

    #--------------------------
    #       HELPER METHODS
    #--------------------------
    def type(self, value):
        return type(value)



