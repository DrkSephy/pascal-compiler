# -*- scanner.py -*-
# -*- MIT Licence (c) 2014 -*-
# -*- drksephy.github.io -*-

def scan(target):
    for char in target:
        print char

KEYWORDS = {
    'AND'       : 'TK_AND',
    'BEGIN'     : 'TK_BEGIN',
    'BREAK'     : 'TK_BREAK',
    'CONST'     : 'TK_CONST',
    'DIV'       : 'TK_DIV',
    'DO'        : 'TK_DO',
    'DOWNTO'    : 'TK_DOWNTO',
    'ELSE'      : 'TK_ELSE',
    'END'       : 'TK_END',
    'FOR'       : 'TK_FOR',
    'FUNCTION'  : 'TK_FUNCTION',
    'IF'        : 'TK_IF',
    'LABEL'     : 'TK_LABEL', 
    'MOD'       : 'TK_MOD',
    'NOT'       : 'TK_NOT',
    'OR'        : 'TK_OR', 
    'PROGRAM'   : 'TK_PROGRAM',
    'REPEAT'    : 'TK_REPEAT',
    'STRING'    : 'TK_STRING', 
    'THEN'      : 'TK_THEN',
    'TO'        : 'TK_TO',
    'TYPE'      : 'TK_TYPE',
    'VAR'       : 'TK_VAR',
    'WHILE'     : 'TK_WHILE'
}