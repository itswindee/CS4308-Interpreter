"""
 * Class:       CS 4308 Section W01
 * Term:        Summer 2024
 * Name:        Emily Zhu
 * Instructor:  Sharon Perry
 * Project:     Deliverable P3 Interpreter
"""

import re

# function
code = """function a()
	x = 1
	while <x 4 do
		x += x 1
	end
	print(x)
end
"""

token_patterns = [
    ('FUNCTION', r'\bfunction\b'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('LITERAL_INTEGER', r'\b\d+\b'),
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
    ('WHILE', r'\bwhile\b'),
    ('DO', r'\bdo\b'),
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

print("Lexical Analysis...")

print(f'{"-" * 40}')
print("Test Input:")
print(f'{"-" * 40}')
print(code)

print(f'{"Lexeme":<15} {"Symbol":<10}')
print(f'{"-" * 15} {"-" * 20}')

tokens = tokenize(code)
for token in tokens:
    print(f'{token[1]:<15} {token[0]}')

print("Lexical Analysis Complete...")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            self.error(f"Parsing error: Expected {token_type}, got {self.current_token[0] if self.current_token else 'EOF'}")

    def error(self, message):
        print(f"{message}")
        exit(1)

    def parse(self):
        print("Syntax Analysis...")
        try:
            self.program()
            print("Syntax Analysis Complete...")
        except Exception as e:
            self.error(str(e))

    def program(self):
        print("<program> -> function id() <block> end")
        self.eat('FUNCTION')
        self.eat('ID')
        self.eat('OPEN_PARENTHESIS')
        self.eat('CLOSE_PARENTHESIS')
        self.block()
        self.eat('END')

    def block(self):
        while self.current_token and self.current_token[0] in ['ID', 'IF', 'WHILE', 'PRINT']:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'ID':
            self.assignment_statement()
        elif self.current_token[0] == 'IF':
            self.if_statement()
        elif self.current_token[0] == 'WHILE':
            self.while_statement()
        elif self.current_token[0] == 'PRINT':
            self.print_statement()
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]}")

    def assignment_statement(self):
        print("<assignment_statement> -> id <assignment_operator> <arithmetic_expression>")
        self.eat('ID')
        self.eat('ASSIGNMENT_OPERATOR')
        self.arithmetic_expression()

    def if_statement(self):
        print("<if_statement> -> if <boolean_expression> then <block> else <block> end")
        self.eat('IF')
        self.boolean_expression()
        self.eat('THEN')
        self.block()
        self.eat('ELSE')
        self.block()
        self.eat('END')

    def while_statement(self):
        print("<while_statement> -> while <boolean_expression> do <block> end")
        self.eat('WHILE')
        self.boolean_expression()
        self.eat('DO')
        self.block()
        self.eat('END')

    def print_statement(self):
        print("<print_statement> -> print(<arithmetic_expression>)")
        self.eat('PRINT')
        self.eat('OPEN_PARENTHESIS')
        self.arithmetic_expression()
        self.eat('CLOSE_PARENTHESIS')

    def boolean_expression(self):
        print("<boolean_expression> -> <relative_op> <arithmetic_expression> <arithmetic_expression>")
        self.relative_op()
        self.arithmetic_expression()
        self.arithmetic_expression()

    def relative_op(self):
        if self.current_token[0] in ['LE_OPERATOR', 'LT_OPERATOR', 'GE_OPERATOR', 'GT_OPERATOR', 'EQ_OPERATOR', 'NE_OPERATOR']:
            print(f"<relative_op> -> {self.current_token[0]}")
            self.eat(self.current_token[0])
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]} in relative_op")

    def arithmetic_expression(self):
        print("<arithmetic_expression> -> id | literal_integer | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>")
        if self.current_token[0] == 'ID':
            self.eat('ID')
        elif self.current_token[0] == 'LITERAL_INTEGER':
            self.eat('LITERAL_INTEGER')
        elif self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            self.arithmetic_op()
            self.arithmetic_expression()
            self.arithmetic_expression()
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]} in arithmetic_expression")

    def arithmetic_op(self):
        if self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            print(f"<arithmetic_op> -> {self.current_token[0]}")
            self.eat(self.current_token[0])
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]} in arithmetic_op")

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def interpret(self):
        self.parser.parse()
        self.program()

    def program(self):
        self.eat('FUNCTION')
        self.eat('ID')
        self.eat('OPEN_PARENTHESIS')
        self.eat('CLOSE_PARENTHESIS')
        self.block()
        self.eat('END')

    def block(self):
        while self.parser.current_token and self.parser.current_token[0] in ['ID', 'IF', 'WHILE', 'PRINT']:
            self.statement()

    def statement(self):
        if self.parser.current_token[0] == 'ID':
            self.assignment_statement()
        elif self.parser.current_token[0] == 'IF':
            self.if_statement()
        elif self.parser.current_token[0] == 'WHILE':
            self.while_statement()
        elif self.parser.current_token[0] == 'PRINT':
            self.print_statement()
        else:
            self.error(f"Runtime error: Unexpected token {self.parser.current_token[0]}")

    def assignment_statement(self):
        var_name = self.parser.current_token[1]
        self.eat('ID')
        self.eat('ASSIGNMENT_OPERATOR')
        value = self.arithmetic_expression()
        self.variables[var_name] = value

    def if_statement(self):
        self.eat('IF')
        condition = self.boolean_expression()
        self.eat('THEN')
        if condition:
            self.block()
        else:
            self.eat('ELSE')
            self.block()
        self.eat('END')

    def while_statement(self):
        self.eat('WHILE')
        while self.boolean_expression():
            self.eat('DO')
            self.block()
        self.eat('END')

    def print_statement(self):
        self.eat('PRINT')
        self.eat('OPEN_PARENTHESIS')
        value = self.arithmetic_expression()
        print(value)
        self.eat('CLOSE_PARENTHESIS')

    def boolean_expression(self):
        operator = self.parser.current_token[0]
        self.eat(operator)
        left = self.arithmetic_expression()
        right = self.arithmetic_expression()
        return self.evaluate_boolean_expression(operator, left, right)

    def evaluate_boolean_expression(self, operator, left, right):
        if operator == 'LE_OPERATOR':
            return left <= right
        elif operator == 'LT_OPERATOR':
            return left < right
        elif operator == 'GE_OPERATOR':
            return left >= right
        elif operator == 'GT_OPERATOR':
            return left > right
        elif operator == 'EQ_OPERATOR':
            return left == right
        elif operator == 'NE_OPERATOR':
            return left != right
        else:
            self.error(f"Runtime error: Unexpected operator {operator} in boolean_expression")

    def arithmetic_expression(self):
        if self.parser.current_token[0] == 'ID':
            var_name = self.parser.current_token[1]
            self.eat('ID')
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                self.error(f"Runtime error: Undefined variable {var_name}")
        elif self.parser.current_token[0] == 'LITERAL_INTEGER':
            value = int(self.parser.current_token[1])
            self.eat('LITERAL_INTEGER')
            return value
        elif self.parser.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            operator = self.parser.current_token[0]
            self.eat(operator)
            left = self.arithmetic_expression()
            right = self.arithmetic_expression()
            return self.evaluate_arithmetic_expression(operator, left, right)
        else:
            self.error(f"Runtime error: Unexpected token {self.parser.current_token[0]} in arithmetic_expression")

    def evaluate_arithmetic_expression(self, operator, left, right):
        if operator == 'ADD_OPERATOR':
            return left + right
        elif operator == 'SUB_OPERATOR':
            return left - right
        elif operator == 'MUL_OPERATOR':
            return left * right
        elif operator == 'DIV_OPERATOR':
            return left / right
        else:
            self.error(f"Runtime error: Unexpected operator {operator} in arithmetic_expression")

    def eat(self, token_type):
        if self.parser.current_token and self.parser.current_token[0] == token_type:
            self.parser.current_token_index += 1
            self.parser.current_token = self.parser.tokens[self.parser.current_token_index] if self.parser.current_token_index < len(self.parser.tokens) else None
        else:
            self.error(f"Runtime error: Expected {token_type}, got {self.parser.current_token[0] if self.parser.current_token else 'EOF'}")

    def error(self, message):
        print(f"{message}")
        exit(1)

# Test the interpreter
tokens = tokenize(code)
parser = Parser(tokens)
interpreter = Interpreter(parser)
interpreter.interpret()
