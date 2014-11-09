# -*- simulator.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#---------------------------------------
#                  TODO
#---------------------------------------

# - [   ] Create code array
# - [   ] Create data array
# - [   ] Create stack array
# - [   ] Implement opcodes
# - [   ] Create simulator 
# - [   ] Build symbol tables

from prettytable import PrettyTable

class Simulator(object):

    def __init__(self, ast, stack, symtable, ip):
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
        self.stack      = stack
        self.symtable   = symtable
        self.ip         = ip


    #--------------------------
    #         SIMULATOR
    #--------------------------
    
    def simulate(self, ast):
        for node in ast:
            print node
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
        # print self.symtable
        print(self.printer(1, ['NUMBER', 'TYPE', 'NAME', 'VALUE', 'ADDRESS'], [], self.symtable))

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

    def op_lesseq(self):
        val = int(self.stack[1]) <= int(self.stack[0])
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



    