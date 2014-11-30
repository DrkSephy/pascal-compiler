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
            print self.ast[self.ip]
            if self.ast[self.ip]['instruction'] == 'push':
                if self.ast[self.ip]['token'] == 'TK_IDENTIFIER':
                    self.pushi(self.ast[self.ip]['value'])
                else:
                    self.push(self.ast[self.ip]['value'])
            if self.ast[self.ip]['instruction'] == 'or':
                self.op_or()
            if self.ast[self.ip]['instruction'] == 'and':
                self.op_and()
            if self.ast[self.ip]['instruction'] == 'xor':
                self.op_xor()
            if self.ast[self.ip]['instruction'] == 'not':
                self.op_not()
            if self.ast[self.ip]['instruction'] == 'mod':
                self.mod()
            if self.ast[self.ip]['instruction'] == 'less':
                self.op_less()
            if self.ast[self.ip]['instruction'] == 'greater':
                self.op_greater()
            if self.ast[self.ip]['instruction'] == 'less_equals':
                self.op_lesseq()
            if self.ast[self.ip]['instruction'] == 'greater_equals':
                self.op_greatereq()
            if self.ast[self.ip]['instruction'] == 'not_equals':
                self.op_noteq()
            if self.ast[self.ip]['instruction'] == 'equals':
                self.op_equals()
            if self.ast[self.ip]['instruction'] == 'div_float':
                self.div_float()
            if self.ast[self.ip]['instruction'] == 'add':
                self.add()
            if self.ast[self.ip]['instruction'] == 'pop':
                self.pop(self.ast[self.ip]['value'])
            if self.ast[self.ip]['instruction'] == 'minus':
                self.minus()
            if self.ast[self.ip]['instruction'] == 'mult':
                self.mult()
            if self.ast[self.ip]['instruction'] == 'halt':
                self.halt()
            print self.stack
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
    def halt(self):
        print "\n[Emulator]: Finished running program"
        print(self.printer(1, ['NUMBER', 'TYPE', 'NAME', 'VALUE', 'ADDRESS'], [], self.symtable))
        sys.exit(0)

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



    