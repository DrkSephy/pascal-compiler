# -*- scanner.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#################
#     TODO      #
#################

# - [done] Scan <target program>
# - [done] Tokenize program
# - [done] Convert code using Classes
# - [done] Create metadata for debugging
# - [    ] Need to tokenize '' ""
# - [    ] Need to tokenize (  )
# - [    ] Need to build system tables
# - [    ] Need to handle comment tokens


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
        ';'         : 'TK_SEMICOLON',
        '('         : 'TK_OPEN_PARENTHESIS',
        ')'         : 'TK_CLOSE_PARENTHESIS',
        '\''        : 'TK_QUOTE'
    }

    SYSTEM = {
        'Writeln'   : 'TK_WRITELN',
        'abs'       : 'TK_ABS'
    }


    def scan(self, source):
    # Reads <source program> and builds tokens. 
        text = open(source, 'r').readlines()
        for line in text:
            for char in line: 
                self.build_string(char)
                if self.to_ascii(char) == 13:
                    self.curr_col = 1
                    self.curr_row += 1
                self.curr_col += 1

        # Print out metadata
        print(self.printer(1, ['NUMBER', 'TOKEN', 'COLUMN', 'VALUE', 'ROW'], [], self.metadata ))




    ############################
    #      HELPER METHODS      #
    ############################

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
            for k, v in datum.items():
                if str(k) == 'TOKEN':
                    storage.append(v)
                if str(k) == 'ROW':
                    storage.append(v)
                if str(k) == 'VALUE':
                    storage.append(v)
                if str(k) == 'COL':
                    storage.append(v)
            table.add_row(storage)
            del storage[:]
            iterator += 1
        return table


    def lookup(self, table, key):
        # Returns: value from table
        #
        # Parameters:
        #   table: dictionary
        #       key, value pairs 
        #   key: string
        #       lookup key 

        return table[key]

    def to_ascii(self, char):
        # Returns: ascii value of char
        # 
        # Parameters:
        #   char: character
        #       character to get ascii value of

        return ord(char)

    def to_lower(self, char):
        # Returns: lowercase string
        #
        # Parameters:
        #   char: character
        #       character to lowercase

        return char.lower()

    def to_upper(self, char):
        # Returns: uppercase string
        # 
        # Parameters:
        #   char: character
        #       character to uppercase

        return char.upper()

    def alphanumberic(self, char):
        # Returns: Boolean
        # 
        # Parameters:
        #   char: character
        #       character to check if alphanumeric
        
        return char.isalpha()

    def build_string(self, char):
        # Based on existing conditions, uses a state-machine
        # approach to determine when and what tokens to build, 
        # using current existing tokens and built string.
        # 
        # Returns: Nothing
        #
        # Parameters: 
        #   char: character
        #       character to build strings with

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

