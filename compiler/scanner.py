# -*- scanner.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#################
#     TODO      #
#################

# - [done] Scan <target program>
# - [    ] Tokenize keywords
# - [done] Convert code using Classes

import sys


class Scanner(object):

    def __init__(self, curr_row, curr_col, curr_token, curr_val, tokens):
        self.curr_row   = curr_row
        self.curr_col   = curr_col
        self.curr_token = curr_token
        self.curr_val   = curr_val
        self.tokens     = tokens


    def scan(self, source):
    # Reads <source program> and builds tokens. 
        text = open(source, 'r').read().splitlines()
        for line in text:
            for char in line: 
                # Treat all ascii chars <= 32 as spaces
                if self.to_ascii(char) == 32:
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char
                # Check if char: ! " # $ % & ' ( ) * + , - . / : ; < = > ? @

                if ((self.to_ascii(char) > 32 and self.to_ascii(char) < 47) or (self.to_ascii(char) > 57 and self.to_ascii(char) < 65)):
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char

                # Check if char: 0 1 2 3 4 5 6 7 8 9
                if self.to_ascii(char) > 47 and self.to_ascii(char) < 58:
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char
                
                # Check if char is uppercase
                if (self.to_ascii(char) > 64 and self.to_ascii(char) < 91):
                    self.build_string(self.to_lower(char))
                    # print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + self.to_lower(char) 
                
                # Check if char is lowercase
                if self.to_ascii(char) > 96 and self.to_ascii(char) < 123:
                    # build_string(char)
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char

                # Check if char: [ \ ] ^ _ `
                if self.to_ascii(char) > 90 and self.to_ascii(char) < 97:
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char

                # Check if char: { | } ~ DEL
                if self.to_ascii(char) > 122 and self.to_ascii(char) < 128:
                    print "row: " + str(self.curr_row) + " , " + "col: " + str(self.curr_col) + " is: " + char
                self.curr_col += 1
            self.curr_row += 1


    ############################
    #      HELPER METHODS      #
    ############################

    def lookup(self, table, key):
        return self.table[key]

    def to_ascii(self, char):
        return ord(char)

    def to_lower(self, char):
        return char.lower()

    def to_upper(self, char):
        return char.upper()

    def build_string(self, char):
        self.curr_val += char
        print self.curr_val


    KEYWORDS = {
        'BEGIN'     : 'TK_BEGIN',
        'BREAK'     : 'TK_BREAK',
        'CONST'     : 'TK_CONST',
        'DO'        : 'TK_DO',
        'DOWNTO'    : 'TK_DOWNTO',
        'ELSE'      : 'TK_ELSE',
        'END'       : 'TK_END',
        'END.'      : 'TK_END_CODE',
        'FOR'       : 'TK_FOR',
        'FUNCTION'  : 'TK_FUNCTION',
        'IDENTIFIER': 'TK_IDENTIFIER',
        'IF'        : 'TK_IF',
        'LABEL'     : 'TK_LABEL', 
        'PROGRAM'   : 'TK_PROGRAM',
        'REPEAT'    : 'TK_REPEAT',
        'STRING'    : 'TK_STRING', 
        'THEN'      : 'TK_THEN',
        'TO'        : 'TK_TO',
        'TYPE'      : 'TK_TYPE',
        'VAR'       : 'TK_VAR',
        'WHILE'     : 'TK_WHILE'
    }

    OPERATORS = {
        '+'         : 'TK_PLUS',
        '-'         : 'TK_MINUS',
        '*'         : 'TK_MULT',
        '/'         : 'TK_DIV_FLOAT',
        'DIV'       : 'TK_DIV',
        'MOD'       : 'TK_MOD',
        ':'         : 'TK_COLON',
        '='         : 'TK_EQUALS',
        ':='        : 'TK_ASSIGNMENT',
        '>'         : 'TK_GREATER',
        '<'         : 'TK_LESS',
        '>='        : 'TK_GREATER_EQUALS',
        '<='        : 'TK_LESS_EQUALS',
        'AND'       : 'TK_AND',
        'OR'        : 'TK_OR',
        'NOT'       : 'TK_NOT'
    }

scanner = Scanner(1, 1, '', '', [])
