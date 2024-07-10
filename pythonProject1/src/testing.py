import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = 0
        self.parse()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, but found {self.current_token[0]}")

    def parse(self):
        while self.current_token:
            if self.current_token[0] == 'FUNCTION':
                self.parse_function_declaration()
            elif self.current_token[0] == 'ID':
                self.parse_assignment()
            elif self.current_token[0] == 'PRINT':
                self.parse_print_statement()
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")

    def parse_function_declaration(self):
        self.expect('FUNCTION')
        self.expect('ID')
        self.expect('OPEN_PARENTHESIS')
        # Parse function parameters (if any)
        while self.current_token[0] != 'CLOSE_PARENTHESIS':
            self.expect('ID')
            # Handle function parameters
        self.expect('CLOSE_PARENTHESIS')
        # Parse function body (statements inside the function)
        while self.current_token[0] != 'END':
            self.parse_statement()
        self.expect('END')

    def parse_assignment(self):
        self.expect('ID')
        self.expect('ASSIGNMENT_OPERATOR')
        # Parse expression on the right-hand side of the assignment
        # Handle variable assignment

    def parse_print_statement(self):
        self.expect('PRINT')
        self.expect('OPEN_PARENTHESIS')
        # Parse expression to be printed
        # Handle print statement
        self.expect('CLOSE_PARENTHESIS')

    def parse_statement(self):
        # Implement parsing for other statements (e.g., conditionals, loops, etc.)
        pass

# Example input code
code = """
function a()
    x = 1
    print(x)
end
"""

# Tokenize the input code
def tokenize(code):
    token_patterns = [
        ('FUNCTION', r'\bfunction\b'),
        ('ID', r'[a-zA-Z]\w*'),
        ('LITERAL_INTEGER', r'\d+'),
        ('ASSIGNMENT_OPERATOR', r'='),
        ('PRINT', r'\bprint\b'),
        ('OPEN_PARENTHESIS', r'\('),
        ('CLOSE_PARENTHESIS', r'\)'),
        ('WHITESPACE', r'\s+'),
        ('COMMENT', r'//.*'),
    ]
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
    token_re = re.compile(token_regex)
    tokens = []
    for match in token_re.finditer(code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type != 'WHITESPACE' and token_type != 'COMMENT':
            tokens.append((token_type, token_value))
    return tokens

tokens = tokenize(code)
parser = Parser(tokens)
# You can add code here to display or process the recognized constructs (e.g., print AST nodes)
