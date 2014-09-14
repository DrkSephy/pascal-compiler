# -*- scanner.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#################
#     TODO      #
#################

# - [done] Scan <target program>
# - [done] Tokenize program
# - [done] Convert code using Classes
# - [    ] Create metadata for debugging
# - [    ] Need to tokenize '' ""
# - [    ] Need to tokenize (  )
# - [    ] Need to build system tables

import sys
from prettytable import PrettyTable


class Scanner(object):

    def __init__(self, curr_row, curr_col, curr_token, curr_val, tokens, metadata):
        self.curr_row   = curr_row
        self.curr_col   = curr_col
        self.curr_token = curr_token
        self.curr_val   = curr_val
        self.tokens     = tokens
        self.metadata   = metadata

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
        'NOT'       : 'TK_NOT',
        ';'         : 'TK_SEMICOLON'
    }


    def scan(self, source):
    # Reads <source program> and builds tokens. 
        text = open(source, 'r').read().splitlines()
        for line in text:
            for char in line: 
                self.build_string(char)
                self.curr_col += 1
            self.curr_row += 1
            self.curr_col = 1


        x = PrettyTable()
        x.field_names = ['NUMBER', 'TOKEN', 'COLUMN', 'VALUE', 'ROW']
        
        i = 1
        datum = []
        for data in self.metadata:
            datum.append(i)
            for k, v in data.items():
                if str(k) == 'TOKEN':
                    datum.append(v)
                if str(k) == 'ROW':
                    datum.append(v)
                if str(k) == 'VALUE':
                    datum.append(v)
                if str(k) == 'COL':
                    datum.append(v)
            x.add_row(datum)
            del datum[:]
            i += 1
        print x
                




    ############################
    #      HELPER METHODS      #
    ############################

    def lookup(self, table, key):
        # Lookup tokens 
        return table[key]

    def to_ascii(self, char):
        # Returns ascii value of char
        return ord(char)

    def to_lower(self, char):
        # Returns lowercase string
        return char.lower()

    def to_upper(self, char):
        # Returns uppercase string
        return char.upper()

    def alphanumberic(self, char):
        # Checks if string is alphanumeric
        # Useful for generating errors in with scanning
        return char.isalpha()

    def build_string(self, char):

        # Character is a space
        if self.to_ascii(char) <= 32: 
            # If current token exists, we append it
            if self.curr_token:
                if self.to_upper(self.curr_val) in self.KEYWORDS:
                    self.curr_token = self.lookup(self.KEYWORDS, self.to_upper(self.curr_val))
                    self.tokens.append(self.curr_token)
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                if self.to_upper(self.curr_val) in self.OPERATORS:
                    self.curr_token = self.lookup(self.OPERATORS, self.to_upper(self.curr_val))
                    self.tokens.append(self.curr_token)
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return 

                if self.to_upper(self.curr_val) not in self.OPERATORS:
                    if self.to_upper(self.curr_val) not in self.KEYWORDS:
                        if self.curr_token == 'TK_COLON':
                            self.tokens.append(self.curr_token)
                            self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : ':', 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                            self.curr_token = ''
                        else: 
                            self.tokens.append(self.curr_token)
                            self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                            return

            # If there is no token and we are looking at spaces, just return
            if not self.curr_token: 
                return

        # Character is a semicolon
        if self.to_ascii(char) == 59:
            # If current token exists, we append it
            if self.curr_token:
                self.tokens.append(self.curr_token)
                self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                self.curr_token = ''
                self.curr_val = '' 

            # If there is no current token, push semicolon token
            if not self.curr_token:
                self.tokens.append('TK_SEMICOLON')
                self.metadata.append({'TOKEN' : 'TK_SEMICOLON', 'VALUE' : ';', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                return

        # Character is colon
        if self.to_ascii(char) == 58:
            # If there is no current token, assign colon token
            if not self.curr_token:
                self.curr_token = 'TK_COLON'
                return

        # Character is equals
        if self.to_ascii(char) == 61:
            # If there is no current token, push equals token
            if not self.curr_token:
                self.tokens.append('TK_EQUALS')
                self.metadata.append({'TOKEN' : 'TK_EQUALS', 'VALUE' : '=', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                return

            # If there is a current token, it must be colon
            if self.curr_token:
                self.tokens.append('TK_ASSIGNMENT')
                self.metadata.append({'TOKEN': 'TK_ASSIGNMENT', 'VALUE' : ':=', 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                self.curr_token = ''
                return

        # Character is a dot
        if self.to_ascii(char) == 46:
            # If there is a current token, it is END
            if self.curr_token:
                self.tokens.append('TK_END_CODE')
                self.metadata.append({'TOKEN': 'TK_END_CODE', 'VALUE' : 'END.', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                self.curr_token = ''
                return


        # If none of the above cases are true, build string
        self.curr_val += char

        # string is not in either table
        if self.to_upper(self.curr_val) not in self.KEYWORDS:
            if self.to_upper(self.curr_val) not in self.OPERATORS:
                self.curr_token = 'TK_IDENTIFIER'

