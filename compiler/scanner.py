# -*- scanner.py -*-
# -*- MIT License (c) 2014 David Leonard -*-
# -*- drksephy.github.io -*-

#----------------------------------------
#  TODO      
#----------------------------------------

# - [done] Scan <target program>
# - [done] Tokenize program
# - [done] Convert code using Classes
# - [done] Create metadata for debugging
# - [done] Need to tokenize '' ""
# - [done] Need to tokenize (  )
# - [done] Need to build system tables
# - [done] Need to handle comment tokens

from prettytable import PrettyTable


class Scanner(object):

    def __init__(self, curr_row, curr_col, curr_token, curr_val, tokens, metadata, comment, string, numeric, real):
        # Parameters
        #   * curr_row  : Integer
        #       - Row token is built
        #   * curr_col  : Integer
        #       - Column token is built   
        #   * curr_token: String
        #       - Current token state
        #   * curr_val  : String
        #       - Current token value
        #   * tokens    : List of tuples
        #       - List of tokens, row, column, value
        #   * metadata  : List of dictionaries
        #       - List of dicts containing token, row, column, value
        #   * comment   : Boolean
        #       - Comment state (Building comments)
        #   * string    : Boolean
        #       - String state (Building strings)
        #   * numeric   : Boolean
        #       - Numeric state (Building integers)
        #   * real      : Boolean
        #       - Real state (Building floats)

        self.curr_row   = curr_row
        self.curr_col   = curr_col
        self.curr_token = curr_token
        self.curr_val   = curr_val
        self.tokens     = tokens
        self.metadata   = metadata
        self.comment    = comment
        self.string     = string
        self.numeric    = numeric
        self.real       = real



    #----------------------------------------
    #               SCANNER                  
    #----------------------------------------

    # Reads source program and build tokens.
     
    # Cycles through the following states:
    #       Comments state -> String state -> 
    #           Numeric state -> Build String state
     
    # Comments state: 
    #       <pre-condition> Entered when we see (*
    #       Determines if we see beginning of comment. 
    #       If we are in comment state, ignore everything
    #       until we see close comment *)
     
    # String state:
    #       <pre-condition> Entered once we see a quote.
    #       Determines if we are building a real string.
    #       Builds the string until we see an end quote. 
    
    # Numeric state:
    #       <pre-condition> Entered once we see a numeric char.
    #       Determines if we are building digit strings.
    #       Depending on symbol we see in this state, we toggle
    #       between building integers and building reals.
    
    # Build String state:
    #       <pre-condition> Entered if we none of above are true.
    #       Contains substates for building the following structures:
    #           * If we see a space, build current token based on tables
    #           * Builds : and := tokens.
    #           * Builds -, +, /, * tokens
    #           * Builds parenthesis, determines if comment being built
    #           * Builds . and end. tokens
    #           * Builds identifiers.  
   

    def scan(self, source):
    # Reads <source program> and builds tokens. 
        text = open(source, 'r').readlines()
        for line in text:
            for char in line: 

                # Handle comments
                if self.comment: 
                    self.handle_comments(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle strings
                elif self.string:
                    self.string_builder(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle digits
                elif self.numeric:
                    self.numeric_builder(char)
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

                # Handle other cases
                else:
                    self.build_string(char)
                    # Handle carriage returns
                    if self.to_ascii(char) == 13:
                        self.curr_col = 1
                        self.curr_row += 1
                    self.curr_col += 1

        # Print out metadata
        print(self.printer(1, ['NUMBER', 'TOKEN', 'COLUMN', 'VALUE', 'ROW'], [], self.metadata ))
        # print(self.tokens)
        return self.tokens




    #----------------------------------------
    #             NUMERIC STATE              
    #----------------------------------------

    # Builds numeric strings

    # <pre-condition> 
    #   * Seen numeric character
    #   * self.numeric : True

    # <post-condition>
    #   * If we see a number, keep building
    #   * If we see a symbol/space, build token
    #       * self.real = False
    #       * self.numeric = False
    #   * If we see (dot), we are building a real
    #       * self.real = True

    def numeric_builder(self, char):
        # If char is a number, keep building number string
        if self.to_ascii(char) >= 48 and self.to_ascii(char) <=57:
            self.curr_val += char

        # Character is a symbol/space, time to build token
        if (self.to_ascii(char) > 57 or self.to_ascii(char) <= 32):
            self.numeric = False
            if self.real: 
                self.tokens.append(('TK_REAL', self.curr_val, self.curr_row, self.curr_col - 1))
                self.metadata.append({'TOKEN' : 'TK_REAL', 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                self.curr_val = ''
                self.real = False
                return
            else: 
                self.tokens.append(( 'TK_INTEGER', self.curr_val, self.curr_row, self.curr_col - 1 ))
                self.metadata.append({ 'TOKEN' : 'TK_INTEGER', 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col - 1 })
                self.curr_val = ''
                return

        # If Character is a dot, it can be a real
        if self.to_ascii(char) == 46: 
            self.curr_val += char
            self.real = True

    #----------------------------------------
    #              STRING STATE              
    #----------------------------------------

    # Builds real strings

    # <pre-condition>
    #   * Seen a quote
    #   * self.string = True

    # <post-condition>
    #   * If we see endquote, we build string
    #       * self.string = False
    #   * Else, keep building string

    def string_builder(self, char):
        # If char is a quote ...
        if self.to_ascii(char) == 39:
            self.curr_val += char
            self.string = False
            self.tokens.append(( 'TK_STRING', self.curr_val, self.curr_row, self.curr_col ))
            self.metadata.append({ 'TOKEN' : 'TK_STRING', 'VALUE' : self.curr_val, 'ROW' : self.curr_row, 'COL' : self.curr_col })
            self.curr_val = ''
            return

        # Char is not a quote, so keep building string 
        else: 
            self.curr_val += char
            return


    #----------------------------------------
    #             COMMENTS STATE             
    #----------------------------------------

    # Builds comments

    # <pre-condition>
    #   * Seen (*
    #   * self.comment = True

    # <post-condition>
    #   * If we see *, might be building *)
    #       * self.curr_token = 'TK_MULT'
    #   * If char is )
    #       * If no current token, just pass
    #   * If current token is *, we build *)
    #       * self.comment = False
    #       * self.curr_token = ''
    #   * Else, we have not ended our comment section

    def handle_comments(self, char):
        # If char is * ...
        if self.to_ascii(char) == 42:
            self.curr_token = 'TK_MULT'
            return

        # If char is ) ...
        if self.to_ascii(char) == 41:
            # If there is no current token
            if not self.curr_token:
                pass
            
            # If there is a current token, it has to be *
            if self.curr_token == 'TK_MULT':
                self.comment = False
                self.tokens.append(('TK_END_COMMENT', '*)', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN' : 'TK_END_COMMENT', 'VALUE' : '*)', 'ROW' : self.curr_row, 'COL' : self.curr_col })
                self.curr_token = '' 

        # We have not yet ended our comment section
        pass

    #----------------------------------------
    #             PRETTY PRINTER             
    #----------------------------------------

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


    #----------------------------------------
    #            HELPER METHODS              
    #----------------------------------------

    def handle_numeric(self, char):
        # Returns: boolean
        #
        # Parameters:
        #   char: character
        #       String to determine if numeric

        return char.isdigit()

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

    def alphanumeric(self, char):
        # Returns: Boolean
        # 
        # Parameters:
        #   char: character
        #       character to check if alphanumeric
        
        return char.isalpha()


    #----------------------------------------
    #               MAIN STATE               
    #----------------------------------------

    # Builds arbitrary character strings

    # <pre-condition>
    #   * Not in comment, string or numeric state

    # <post-condition>
    #   * If we see a space, build token from table
    #       * If token not in table, mark as identifier
    #   * If we see * 
    #       * self.curr_token = 'TK_MULT'
    #       * If we have seen (, build (*
    #           * self.comment = True
    #   * If we see :
    #       * self.curr_token = 'TK_COLON'
    #       * If we see =
    #           * build 'TK_ASSIGNMENT'
    #       * Else build colon token
    #   * If we see ;, build semicolon token
    #   * If we see a digit
    #       * self.numeric = True
    #   * If we see open quote
    #       * self.string = True
    #   * If we see +, -, /, *, build token
    #   * If we see .
    #       * self.curr_token = 'TK_DOT'
    #       * If we have seen END
    #           * build 'TK_END.'
    #       * Else build 'TK_DOT' token
    #   * Else concatenate string, mark as identifier
    #       * If cycle repeats and not in any table, we
    #         build token as an identifier when we see a 
    #         space, symbol or digit

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


        #----------------------------------------
        #             SPACE SUBSTATE             
        #----------------------------------------

        if self.to_ascii(char) <= 32: 
            # If current token exists, we append it
            if self.curr_token:
                print self.curr_token
                if self.to_upper(self.curr_val) in self.KEYWORDS:
                    self.curr_token = self.lookup(self.KEYWORDS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                if self.to_upper(self.curr_val) in self.OPERATORS:
                    print "Building: " + self.to_upper(self.curr_val)
                    self.curr_token = self.lookup(self.OPERATORS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col - 1))   
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return 

                if self.to_upper(self.curr_val) in self.SYSTEM: 
                    self.curr_token = self.lookup(self.SYSTEM, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    return

                # Current token value is not in any table
                if self.to_upper(self.curr_val) not in self.OPERATORS:
                    if self.to_upper(self.curr_val) not in self.KEYWORDS:
                        if self.curr_token == 'TK_COLON':
                            self.tokens.append((self.curr_token, ':', self.curr_row, self.curr_col - 1))
                            self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : ':', 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                        elif self.curr_token == 'TK_OPEN_PARENTHESIS':
                            self.tokens.append((self.curr_token, '(', self.curr_row, self.curr_col - 1))
                            self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : '(', 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                        else: 
                            self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col -1))
                            self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                            self.curr_token = ''
                            self.curr_val = ''
                            return

            # If there is no token and we are looking at spaces, just return
            if not self.curr_token: 
                return

        #----------------------------------------
        #           SEMICOLON SUBSTATE           
        #----------------------------------------

        # Character is a semicolon
        if self.to_ascii(char) == 59 and not self.numeric:
            # If current token exists, we append it
            if self.curr_token:
                # If current token value is a keyword....
                if self.to_upper(self.curr_val) in self.KEYWORDS:
                    self.curr_token = self.lookup(self.KEYWORDS, self.to_upper(self.curr_val))
                    self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col - 1))
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = ''
                    
                # If current token is not a keyword...
                # It is currently treated as an identifier
                else: 
                    self.tokens.append((self.curr_token, self.to_lower(self.curr_val), self.curr_row, self.curr_col -1))
                    self.metadata.append({'TOKEN' : self.curr_token, 'VALUE' : self.to_lower(self.curr_val), 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                    self.curr_token = ''
                    self.curr_val = '' 

            # If there is no current token, push semicolon token
            if not self.curr_token:
                self.tokens.append(('TK_SEMICOLON', ';', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN' : 'TK_SEMICOLON', 'VALUE' : ';', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                return

        #----------------------------------------
        #           LESS THAN SUBSTATE              
        #----------------------------------------

        # Character is <
        if self.to_ascii(char) == 60:
            if not self.curr_token:
                self.curr_token = 'TK_LESS'


        #----------------------------------------
        #           GREATER THAN SUBSTATE              
        #----------------------------------------

        # Character is >
        if self.to_ascii(char) == 62:
            if not self.curr_token:
                self.curr_token = 'TK_GREATER'


        #----------------------------------------
        #           EXCLAMATION SUBSTATE              
        #----------------------------------------

        # Character is !
        if self.to_ascii(char) == 33:
            if not self.curr_token:
                self.curr_token = 'TK_EXCLAMATION'

        #----------------------------------------
        #             COLON SUBSTATE              
        #----------------------------------------

        # Character is colon
        if self.to_ascii(char) == 58:
            # If there is no current token, assign colon token
            if not self.curr_token:
                self.curr_token = 'TK_COLON'
                return


        #----------------------------------------
        #             EQUALS SUBSTATE            
        #----------------------------------------

        # Character is equals
        if self.to_ascii(char) == 61:
            # If there is no current token, push equals token
            if not self.curr_token:
                self.tokens.append(('TK_EQUALS', '=', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN' : 'TK_EQUALS', 'VALUE' : '=', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                self.curr_token = ''
                return

            # If there is a current token, it can either be a colon, less than, or greater than
            if self.curr_token == 'TK_COLON':
                self.tokens.append(('TK_ASSIGNMENT', ':=', self.curr_row, self.curr_col -1))
                self.metadata.append({'TOKEN': 'TK_ASSIGNMENT', 'VALUE' : ':=', 'ROW' : self.curr_row, 'COL' : self.curr_col - 1})
                self.curr_token = ''
                return


        #----------------------------------------
        #              DOT SUBSTATE              
        #----------------------------------------

        # Character is a dot
        if self.to_ascii(char) == 46:
            # If there is a current token, it is END
            if self.curr_token:
                self.tokens.append(('TK_END_CODE', 'end.', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN': 'TK_END_CODE', 'VALUE' : 'end.', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                self.curr_token = ''
                return

        #----------------------------------------
        #              COMMA SUBSTATE              
        #----------------------------------------

        # Character is a comma
        if self.to_ascii(char) == 44:
            self.tokens.append(('TK_COMMA', ',', self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN': 'TK_COMMA', 'VALUE': ',', 'ROW' : self.curr_row, 'COL' : self.curr_col })
            self.curr_token = ''
            return

        #----------------------------------------
        #       OPEN PARENTHESIS SUBSTATE        
        #----------------------------------------

        # Character is left parenthesis
        if self.to_ascii(char) == 40:
            if self.curr_token:
                self.tokens.append(('TK_OPEN_PARENTHESIS', '(', self.curr_row, self.curr_col - 1))
                self.metadata.append({'TOKEN' : 'TK_OPEN_PARENTHESIS', 'VALUE' : '(', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                self.curr_token = ''

            # Possible to be start of comment, store token
            if not self.curr_token:
                self.curr_token = 'TK_OPEN_PARENTHESIS'
                return

        #----------------------------------------
        #              MULT SUBSTATE             
        #----------------------------------------

        # Character is *
        if self.to_ascii(char) == 42:
            # If there is no current token, push * token
            if not self.curr_token:
                self.tokens.append(('TK_MULT', '*', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN' : 'TK_MULT', 'VALUE' : '*', 'ROW' : self.curr_row, 'COL' : self.curr_col})
                return

            # If there is a current token, it must form (*
            if self.curr_token:
                self.tokens.append(('TK_BEGIN_COMMENT', '(*', self.curr_row, self.curr_col))
                self.metadata.append({'TOKEN' : 'TK_BEGIN_COMMENT', 'VALUE' : '(*', 'ROW': self.curr_row, 'COL' : self.curr_col})
                self.curr_token = ''
                self.comment = True
                return


        #----------------------------------------
        #        CLOSE PARENTHESIS SUBSTATE      
        #----------------------------------------

        # Character is right parenthesis
        if self.to_ascii(char) == 41:
            # We are not handling a comment, so push token
            self.tokens.append(('TK_CLOSE_PARENTHESIS', ')', self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN' : 'TK_CLOSE_PARENTHESIS', 'VALUE' : ')', 'ROW' : self.curr_row, 'COL' : self.curr_col})
            self.curr_val = ''
            return

        #----------------------------------------
        #           BEGIN QUOTE SUBSTATE         
        #----------------------------------------

        # Character is ' (open quote)
        if self.to_ascii(char) == 39: 
            self.string = True
            self.curr_val += char
            return

        #----------------------------------------
        #       BEGIN DIGIT STRING SUBSTATE      
        #----------------------------------------

        # Character is a digit
        if self.handle_numeric(char):
            self.numeric = True 
            self.curr_val += char
            return 

        #----------------------------------------
        #              PLUS SUBSTATE             
        #----------------------------------------

        # Character is plus 
        if self.to_ascii(char) == 43:
            self.tokens.append(('TK_PLUS', '+', self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN' : 'TK_PLUS', 'VALUE' : '+', 'ROW' : self.curr_row, 'COL' : self.curr_col})
            self.curr_val = ''
            return 

        #----------------------------------------
        #            MINUS SUBSTATE              
        #----------------------------------------

        # Character is minus 
        if self.to_ascii(char) == 45:
            self.tokens.append(('TK_MINUS', '-', self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN' : 'TK_MINUS', 'VALUE' : '-', 'ROW' : self.curr_row, 'COL' : self.curr_col})
            self.curr_val = ''
            return

        #----------------------------------------
        #              DIV SUBSTATE              
        #----------------------------------------

        # Character is /
        if self.to_ascii(char) == 47:
            self.tokens.append(('TK_DIV_FLOAT', '/', self.curr_row, self.curr_col))
            self.metadata.append({'TOKEN' : 'TK_DIV_FLOAT', 'VALUE' : '/', 'ROW' : self.curr_row, 'COL' : self.curr_col})
            self.curr_val = ''
            return

        #----------------------------------------
        #          IDENTIFIER SUBSTATE           
        #----------------------------------------

        # If none of the above cases are true, build string
        self.curr_val += char
        # string is not in either table
        if self.to_upper(self.curr_val) not in self.KEYWORDS:
            if self.to_upper(self.curr_val) not in self.OPERATORS:
                if self.to_upper(self.curr_val) not in self.SYSTEM: 
                    self.curr_token = 'TK_IDENTIFIER'


    #----------------------------------------
    #               TABLES                   
    #----------------------------------------

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
        'WHILE'     : 'TK_WHILE',
        'INTEGER'   : 'TK_ID_INTEGER', 
        'REAL'      : 'TK_ID_REAL',
        'CHAR'      : 'TK_ID_CHAR',
        'BOOLEAN'   : 'TK_ID_BOOLEAN'
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
        '!'         : 'TK_EXCLAMATION',
        '!='        : 'TK_NOT_EQUALS',
        'AND'       : 'TK_AND',
        'OR'        : 'TK_OR',
        'NOT'       : 'TK_NOT',
        ';'         : 'TK_SEMICOLON',
        '('         : 'TK_OPEN_PARENTHESIS',
        ')'         : 'TK_CLOSE_PARENTHESIS',
        '\''        : 'TK_QUOTE',
        '(*'        : 'TK_BEGIN_COMMENT',
        '*)'        : 'TK_END_COMMENT',
        ','         : 'TK_COMMA'
    }

    SYSTEM = {
        'WRITELN'   : 'TK_WRITELN',
        'ABS'       : 'TK_ABS'
    }

