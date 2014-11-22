tokens = [
    ('TK_PROGRAM', 'program', 1, 7), 
    ('TK_VAR', 'var', 3, 4), 
    ('TK_IDENTIFIER', 'x', 3, 6), 
    ('TK_COLON', ':', 3, 8), 
    ('TK_ID_INTEGER', 'integer', 3, 16), 
    ('TK_SEMICOLON', ';', 3, 17), 
    ('TK_BEGIN', 'begin', 5, 6), 
    ('TK_IDENTIFIER', 'x', 6, 6), 
    ('TK_ASSIGNMENT', ':=', 6, 8), 
    ('TK_INTEGER', '17', 6, 12), 
    ('TK_SEMICOLON', ';', 6, 14), 
    ('TK_REPEAT', 'repeat', 7, 11), 
    ('TK_IDENTIFIER', 'x', 8, 10), 
    ('TK_ASSIGNMENT', ':=', 8, 12), 
    ('TK_IDENTIFIER', 'x', 8, 15), 
    ('TK_PLUS', '+', 8, 17), 
    ('TK_INTEGER', '1', 8, 19), 
    ('TK_SEMICOLON', ';', 8, 21), 
    ('TK_UNTIL', 'until', 9, 10), 
    ('TK_IDENTIFIER', 'x', 9, 12), 
    ('TK_GREATER', '>', 9, 14), 
    ('TK_INTEGER', '100', 9, 18), 
    ('TK_SEMICOLON', ';', 9, 20), 
    ('TK_END_CODE', 'end.', 10, 5), 
    ('EOF', 0, 0, 0)]


for token in tokens:
    print token

token_list = iter(tokens)

