# -*- scanner.py -*-
# -*- MIT Licence (c) 2014 -*-
# -*- drksephy.github.io -*-

import sys

def scan(source):
    # Reads <source program> and builds tokens. 

    # Variables to assist with tokenization
    # row/col of current character
    curr_row = 1
    curr_col = 0
    # Current value of token
    curr_val = 0
    # Curent token
    curr_token = 0

    text = open(source, 'r').read().splitlines()
    for line in text:
        print "row #: " + str(curr_row) + ":" + line
        curr_row += 1

        


def lookup(table, key):
    # Reads token value from corresponding table
    return table[key]

def to_ascii(char):
    # Returns ascii value of a character
    return ord(char)


KEYWORDS = {
    'BEGIN'     : 'TK_BEGIN',
    'BREAK'     : 'TK_BREAK',
    'CONST'     : 'TK_CONST',
    'DO'        : 'TK_DO',
    'DOWNTO'    : 'TK_DOWNTO',
    'ELSE'      : 'TK_ELSE',
    'END'       : 'TK_END',
    'FOR'       : 'TK_FOR',
    'FUNCTION'  : 'TK_FUNCTION',
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
    'div'       : 'TK_DIV',
    'mod'       : 'TK_MOD', 
    '='         : 'TK_EQUALS',
    '>'         : 'TK_GREATER',
    '<'         : 'TK_LESS',
    '>='        : 'TK_GREATER_EQUALS',
    '<='        : 'TK_LESS_EQUALS',
    'AND'       : 'TK_AND',
    'OR'        : 'TK_OR',
    'NOT'       : 'TK_NOT'
}