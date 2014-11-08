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
                self.push(node['value'])
            if node['instruction'] == 'add':
                self.add()
            if node['instruction'] == 'pop':
                self.pop(node['value'])
            print self.stack


    #--------------------------
    #         OP CODES
    #--------------------------
    def push(self, value):
        self.stack.insert(0, value)
        return

    def pop(self, value):
        for var in self.symtable:
            print var
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



    