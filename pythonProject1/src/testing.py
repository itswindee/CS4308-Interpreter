import re

# Scanner code (as provided)
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

# Parser code
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse(self):
        try:
            self.program()
            if self.current_token is not None:
                self.error('EOF')
            print("Parsing completed successfully.")
        except SyntaxError as e:
            print(f"Syntax error: {e}")

    def program(self):
        if self.current_token[0] == 'FUNCTION':
            self.next_token()
            if self.current_token[0] == 'ID':
                self.next_token()
                if self.current_token[0] == 'OPEN_PARENTHESIS':
                    self.next_token()
                    if self.current_token[0] == 'CLOSE_PARENTHESIS':
                        self.next_token()
                        self.block()
                        if self.current_token[0] == 'END':
                            self.next_token()
                            print("Program recognized")
                        else:
                            self.error('END')
                    else:
                        self.error('CLOSE_PARENTHESIS')
                else:
                    self.error('OPEN_PARENTHESIS')
            else:
                self.error('ID')
        else:
            self.error('FUNCTION')

    def block(self):
        while self.current_token and self.current_token[0] != 'END' and self.current_token[0] != 'ELSE' and self.current_token[0] != 'UNTIL':
            self.statement()

    def statement(self):
        if self.current_token[0] == 'IF':
            self.if_statement()
        elif self.current_token[0] == 'ID':
            self.assignment_statement()
        elif self.current_token[0] == 'WHILE':
            self.while_statement()
        elif self.current_token[0] == 'PRINT':
            self.print_statement()
        elif self.current_token[0] == 'REPEAT':
            self.repeat_statement()
        else:
            self.error('STATEMENT')

    def if_statement(self):
        self.next_token()
        self.boolean_expression()
        if self.current_token[0] == 'THEN':
            self.next_token()
            self.block()
            if self.current_token[0] == 'ELSE':
                self.next_token()
                self.block()
                if self.current_token[0] == 'END':
                    self.next_token()
                    print("If statement recognized")
                else:
                    self.error('END')
            else:
                self.error('ELSE')
        else:
            self.error('THEN')

    def while_statement(self):
        self.next_token()
        self.boolean_expression()
        if self.current_token[0] == 'DO':
            self.next_token()
            self.block()
            if self.current_token[0] == 'END':
                self.next_token()
                print("While statement recognized")
            else:
                self.error('END')
        else:
            self.error('DO')

    def assignment_statement(self):
        self.next_token()
        if self.current_token[0] == 'ASSIGNMENT_OPERATOR':
            self.next_token()
            self.arithmetic_expression()
            print("Assignment statement recognized")
        else:
            self.error('ASSIGNMENT_OPERATOR')

    def repeat_statement(self):
        self.next_token()
        self.block()
        if self.current_token[0] == 'UNTIL':
            self.next_token()
            self.boolean_expression()
            print("Repeat statement recognized")
        else:
            self.error('UNTIL')

    def print_statement(self):
        self.next_token()
        if self.current_token[0] == 'OPEN_PARENTHESIS':
            self.next_token()
            self.arithmetic_expression()
            if self.current_token[0] == 'CLOSE_PARENTHESIS':
                self.next_token()
                print("Print statement recognized")
            else:
                self.error('CLOSE_PARENTHESIS')
        else:
            self.error('OPEN_PARENTHESIS')

    def boolean_expression(self):
        self.relative_op()
        self.arithmetic_expression()
        self.arithmetic_expression()

    def relative_op(self):
        if self.current_token[0] in ['LE_OPERATOR', 'LT_OPERATOR', 'GE_OPERATOR', 'GT_OPERATOR', 'EQ_OPERATOR', 'NE_OPERATOR']:
            self.next_token()
        else:
            self.error('RELATIVE_OPERATOR')

    def arithmetic_expression(self):
        if self.current_token[0] in ['ID', 'LITERAL_INTEGER']:
            self.next_token()
        elif self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            self.next_token()
            self.arithmetic_expression()
            self.arithmetic_expression()
        else:
            self.error('ARITHMETIC_EXPRESSION')

    def error(self, expected):
        raise SyntaxError(f"Expected {expected} but found {self.current_token}")

# Test the parser
code = """function a()
    x = 1
    print(x)
end
"""

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()

