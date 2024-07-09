"""
 * Class:       CS 4308 Section W01
 * Term:        Summer 2024
 * Name:        Emily Zhu
 * Instructor:  Sharon Perry
 * Project:     Deliverable P1 Scanner
"""

import re

# function
code = """function b()
   y = 2 + 3
   if y == 5 then
       print(10)
   else
       print(1)
   end
end
"""

# token patterns for the lexical analyzer
token_patterns = [
    ('FUNCTION', r'\bfunction\b'),
    ('ID', r'[a-zA-Z]\w*'),
    ('LITERAL_INTEGER', r'\d+'),
    ('ASSIGNMENT_OPERATOR', r'='),
    ('LE_OPERATOR', r'<='),
    ('LT_OPERATOR', r'<'),
    ('GE_OPERATOR', r'>='),
    ('GT_OPERATOR', r'>'),
    ('EQ_OPERATOR', r'=='),
    ('NE_OPERATOR', r'~='),
    ('ADD_OPERATOR', r'\+'),
    ('SUB_OPERATOR', r'-'),
    ('MUL_OPERATOR', r'\*'),
    ('DIV_OPERATOR', r'/'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('THEN', r'\bthen\b'),
    ('END', r'\bend\b'),
    ('PRINT', r'\bprint\b'),
    ('OPEN_PARENTHESIS', r'\('),
    ('CLOSE_PARENTHESIS', r'\)'),
    ('WHITESPACE', r'\s+'),
    ('COMMENT', r'//.*'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
token_re = re.compile(token_regex)

def tokenize(code):
    tokens = []
    for match in token_re.finditer(code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type != 'WHITESPACE' and token_type != 'COMMENT':  # Ignore whitespace and comments
            tokens.append((token_type, token_value))
    return tokens

# print statements to make code look organized
# this is the test input
print(f'{"-" * 40}')
print("Test Input:")
print(f'{"-" * 40}')
print(code)

# this is for the lexeme and symbol
print(f'{"Lexeme":<15} {"Symbol":<10}')
print(f'{"-" * 15} {"-" * 20}')

tokens = tokenize(code)
for token in tokens:
    print(f'{token[1]:<15} {token[0]}')

# PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[0]

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.tokens.pop(0)
            if self.tokens:
                self.current_token = self.tokens[0]
            else:
                self.current_token = None
        else:
            self.error()

    def program(self):
        while self.current_token:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'FUNCTION':
            self.function_declaration()
            print("Function declaration recognized")
        elif self.current_token[0] == 'IF':
            self.if_statement()
            print("If statement recognized")
        elif self.current_token[0] == 'PRINT':
            self.print_statement()
            print("Print statement recognized")
        elif self.current_token[0] == 'ID':
            self.assignment_statement()
            print("Assignment statement recognized")
        else:
            self.error()

    def function_declaration(self):
        self.eat('FUNCTION')
        self.eat('ID')
        self.eat('OPEN_PARENTHESIS')
        self.eat('CLOSE_PARENTHESIS')
        self.block()
        self.eat('END')

    def if_statement(self):
        self.eat('IF')
        self.expression()
        self.eat('THEN')
        self.block()
        if self.current_token and self.current_token[0] == 'ELSE':
            self.eat('ELSE')
            self.block()

    def print_statement(self):
        self.eat('PRINT')
        self.eat('OPEN_PARENTHESIS')
        self.expression()
        self.eat('CLOSE_PARENTHESIS')

    def assignment_statement(self):
        self.eat('ID')
        self.eat('ASSIGNMENT_OPERATOR')
        self.expression()

    def block(self):
        while self.current_token and self.current_token[0] not in ['END', 'ELSE']:
            self.statement()

    def expression(self):
        self.term()
        while self.current_token and self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR']:
            self.eat(self.current_token[0])
            self.term()

    def term(self):
        self.factor()
        while self.current_token and self.current_token[0] in ['MUL_OPERATOR', 'DIV_OPERATOR']:
            self.eat(self.current_token[0])
            self.factor()

    def factor(self):
        if self.current_token[0] == 'ID':
            self.eat('ID')
        elif self.current_token[0] == 'LITERAL_INTEGER':
            self.eat('LITERAL_INTEGER')
        else:
            self.eat('OPEN_PARENTHESIS')
            self.expression()
            self.eat('CLOSE_PARENTHESIS')


# Test the parser
code1 = """function b()
   y = 2 + 3
   if y == 5 then
       print(10)
   else
       print(1)
   end
end
"""

code2 = """print(10)
"""

code3 = """x = 5
if x == 5 then
    print(10)
else
    print(1)
end
"""

codes = [code1, code2, code3]

for code in codes:
    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.program()
    print()


