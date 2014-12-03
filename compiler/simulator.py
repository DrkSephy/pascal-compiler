# -*- simulator.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#---------------------------------------
#                  TODO
#---------------------------------------

# - [done] Create code array
# - [done] Create data array
# - [done] Create stack array
# - [done] Implement opcodes
# - [done] Create simulator 
# - [done] Build symbol tables

import sys
from prettytable import PrettyTable

class Simulator(object):

    def __init__(self, ast, symtable):
        # Paramaters
        #   * ast : List
        #       - Abstract Syntax Tree returned by Parser
        #   * stack : List
        #       - Stack of operands
        #   * symtable: List
        #       - List of all allocated variables
        #   * ip: Integer
        #       - Points to current instruction address
        self.ast        = ast
        self.stack      = []
        self.symtable   = symtable
        self.ip         = 0


    #--------------------------
    #         SIMULATOR
    #--------------------------
    
    def simulate(self):
        while True: 
            print "Current IP is: " + str(self.ip)
            print self.ast[self.ip]
            
            if self.ast[self.ip]['instruction'] == 'op_push':
                if self.ast[self.ip]['token'] == 'TK_IDENTIFIER':
                    self.pushi(self.ast[self.ip]['value'])
                else:
                    self.push(self.ast[self.ip]['value'])
            elif self.ast[self.ip]['instruction'] == 'op_or':
                self.op_or()
            elif self.ast[self.ip]['instruction'] == 'op_and':
                self.op_and()
            elif self.ast[self.ip]['instruction'] == 'op_xor':
                self.op_xor()
            elif self.ast[self.ip]['instruction'] == 'op_not':
                self.op_not()
            elif self.ast[self.ip]['instruction'] == 'op_mod':
                self.mod()
            elif self.ast[self.ip]['instruction'] == 'op_less':
                self.op_less()
            elif self.ast[self.ip]['instruction'] == 'op_greater':
                self.op_greater()
            elif self.ast[self.ip]['instruction'] == 'op_less_equals':
                self.op_lesseq()
            elif self.ast[self.ip]['instruction'] == 'op_greater_equals':
                self.op_greatereq()
            elif self.ast[self.ip]['instruction'] == 'op_not_equals':
                self.op_noteq()
            elif self.ast[self.ip]['instruction'] == 'op_equals':
                self.op_equals()
            elif self.ast[self.ip]['instruction'] == 'op_div_float':
                self.div_float()
            elif self.ast[self.ip]['instruction'] == 'op_add':
                self.add()
            elif self.ast[self.ip]['instruction'] == 'op_pop':
                self.pop(self.ast[self.ip]['value'])
            elif self.ast[self.ip]['instruction'] == 'op_minus':
                self.minus()
            elif self.ast[self.ip]['instruction'] == 'op_mult':
                self.mult()
            elif self.ast[self.ip]['instruction'] == 'op_halt':
                self.halt()
            elif self.ast[self.ip]['instruction'] == 'op_jfalse':
                self.op_jfalse(self.ast[self.ip]['value'])
            elif self.ast[self.ip]['instruction'] == 'op_jmp':
                self.op_jmp(self.ast[self.ip]['value'])
            elif self.ast[self.ip]['instruction'] == 'op_jtrue':
                self.op_jtrue(self.ast[self.ip]['value'])
            else:
                print "Instruction does not exist"
            print self.stack
            
            print "\n"
            self.ip += 1

    #----------------------------------------
    #             PRETTY PRINTER             
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
    def op_jfalse(self, instruction):
        bool_val = self.stack.pop()
        if bool_val == False:
            self.ip = instruction - 1 

    def op_jmp(self, instruction):
        self.ip = instruction - 1 

    def op_jtrue(self, instruction):
        bool_val = self.stack.pop()
        if bool_val == True:
            self.ip = instruction - 1 

    def halt(self):
        print "\n[Emulator]: Finished running program"
        print(self.printer(1, ['NUMBER', 'TYPE', 'NAME', 'VALUE', 'ADDRESS'], [], self.symtable))
        sys.exit(0)

    def op_lesseq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) <= int(op_2)
        self.push(val)
        return

    def op_noteq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) != int(op_2)
        self.push(val)
        return

    def op_equals(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) == int(op_2)
        self.push(val)
        return

    def op_greatereq(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) >= int(op_2)
        self.push(val)
        return


    def op_greater(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) > int(op_2)
        self.push(val)
        return

    def op_less(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) < int(op_2)
        self.push(val)
        return 

    def op_not(self):
        op_1 = self.stack.pop()
        val = not int(op_1)
        self.push(val)
        return 

    def op_and(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) and int(op_1)
        self.push(val)
        return

    def op_xor(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) ^ int(op_1)
        self.push(val)
        return

    def op_or(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) or int(op_1)
        self.push(val)
        return

    def mod(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) % int(op_1)
        self.push(val)
        return 

    def div_float(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_1) / int(op_2)
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
        print value
        op_1 = self.stack.pop()
        for var in self.symtable:
            if var['NAME'] == value:
                var['VALUE'] = op_1
        return

    def mult(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) * int(op_1)
        self.push(val)
        return

    def add(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) + int(op_1)
        self.push(val)
        return


    def minus(self):
        op_1 = self.stack.pop()
        op_2 = self.stack.pop()
        val = int(op_2) - int(op_1)
        self.push(val)
        return

    #--------------------------
    #       HELPER METHODS
    #--------------------------
    def type(self, value):
        return type(value)



    