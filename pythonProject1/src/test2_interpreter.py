"""
 * Class:       CS 4308 Section W01
 * Term:        Summer 2024
 * Name:        Emily Zhu
 * Instructor:  Sharon Perry
 * Project:     Deliverable P3 Interpreter
"""


import re

# Token patterns for the lexical analyzer
token_patterns = [
    ('FUNCTION', r'\bfunction\b'),
    ('ID', r'\b[a-zA-Z]\b'),
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

# function
code = """function a()
    x = 1
    while < x 4 do
        x += x 1
    end
    print(x)
end
"""

print(f'{"-" * 40}')
print("Test Input:")
print(f'{"-" * 40}')
print(code)

# This is for the lexeme and symbol
print(f'{"Lexeme":<15} {"Symbol":<10}')
print(f'{"-" * 15} {"-" * 20}')

tokens = tokenize(code)
for token in tokens:
    print(f'{token[1]:<15} {token[0]}')

print("Lexical Analysis Complete...")

class Parser:
    # sets current token index to 0 and then
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    # this will eat a token of a specified type
    # if the current token matches the expected token, it will move onto the next token
    # if not, it will throw an error message
    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(
                self.tokens) else None
        else:
            self.error(f"Parsing error: Expected {token_type}, got {self.current_token[0]}")

    def error(self, message):
        print(f"{message}")
        exit(1)

    # represents the parsing process & any exceptions
    def parse(self):
        print()
        print("Syntax Analysis...")
        try:
            self.program()
            print("Syntax Analysis Complete...")
        except Exception as e:
            self.error(str(e))

    # this will parse function id() <block> end
    def program(self):
        print("<program> -> function id() <block> end")
        self.eat('FUNCTION')
        self.eat('ID')
        self.eat('OPEN_PARENTHESIS')
        self.eat('CLOSE_PARENTHESIS')
        self.block()
        self.eat('END')

    # this will parse strings/statements
    def block(self):
        if self.current_token and self.current_token[0] in ['ID', 'IF', 'WHILE', 'PRINT']:
            self.statement()
            self.block()
        else:
            return

    # this will determine the string's type and choose the appropriate method
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

    # this will parse an assignment statement: id = <arithmetic_expression>
    def assignment_statement(self):
        print("<assignment_statement> -> id <assignment_operator> <arithmetic_expression>")
        self.eat('ID')
        self.eat('ASSIGNMENT_OPERATOR')
        self.arithmetic_expression()

    # this will parse an if statement: if <boolean_expression> then <block> else <block> end
    def if_statement(self):
        print("<if_statement> -> if <boolean_expression> then <block> else <block> end")
        self.eat('IF')
        self.boolean_expression()
        self.eat('THEN')
        self.block()
        self.eat('ELSE')
        self.block()
        self.eat('END')

    # this will parse a while statement: while <boolean_expression> do <block> end
    def while_statement(self):
        print("<while_statement> -> while <boolean_expression> do <block> end")
        self.eat('WHILE')
        self.boolean_expression()
        self.eat('DO')
        self.block()
        self.eat('END')

    # this will parse a print statement: print(<arithmetic_expression>)
    def print_statement(self):
        print("<print_statement> -> print(<arithmetic_expression>)")
        self.eat('PRINT')
        self.eat('OPEN_PARENTHESIS')
        self.arithmetic_expression()
        self.eat('CLOSE_PARENTHESIS')

    # this will a boolean expression: <relative_op> <arithmetic_expression> <arithmetic_expression>
    def boolean_expression(self):
        print("<boolean_expression> -> <arithmetic_expression> <relative_op> <arithmetic_expression>")
        self.arithmetic_expression()
        self.relative_op()
        self.arithmetic_expression()

    # this will parse operators: <, <=, >, >=, ==, !=
    def relative_op(self):
        if self.current_token[0] in ['LE_OPERATOR', 'LT_OPERATOR', 'GE_OPERATOR', 'GT_OPERATOR', 'EQ_OPERATOR',
                                     'NE_OPERATOR']:
            print(f"<relative_op> -> {self.current_token[0]}")
            self.eat(self.current_token[0])
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]} in relative_op")

    # this will parse an arithmetic expression: id | literal_integer | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>
    def arithmetic_expression(self):
        print(
            "<arithmetic_expression> -> id | literal_integer | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>")
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

    # this will parse an arithmetic operator: one of +, -, *, /
    def arithmetic_op(self):
        if self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            print(f"<arithmetic_op> -> {self.current_token[0]}")
            self.eat(self.current_token[0])
        else:
            self.error(f"Parsing error: Unexpected token {self.current_token[0]} in arithmetic_op")

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()

# Interpreter
class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.variables = {}  # To store variables and their values

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            self.error(f"Parsing error: Expected {token_type}, got {self.current_token[0]}")

    def error(self, message):
        print(f"{message}")
        exit(1)

    def interpret(self):
        print()
        print("Execution Start...")
        try:
            self.program()
            print("Execution Complete...")
        except Exception as e:
            self.error(str(e))

    def program(self):
        self.eat('FUNCTION')
        function_name = self.current_token[1]
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
        elif self.current_token[0] == 'PRINT':
            self.print_statement()
        elif self.current_token[0] == 'IF':
            self.if_statement()
        elif self.current_token[0] == 'WHILE':
            self.while_statement()
        else:
            self.error(f"Execution error: Unexpected token {self.current_token[0]}")

    def assignment_statement(self):
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('ASSIGNMENT_OPERATOR')
        value = self.arithmetic_expression()
        self.variables[var_name] = value

    def print_statement(self):
        self.eat('PRINT')
        self.eat('OPEN_PARENTHESIS')
        value = self.arithmetic_expression()
        print(value)
        self.eat('CLOSE_PARENTHESIS')

    def if_statement(self):
        self.eat('IF')
        condition = self.boolean_expression()
        self.eat('THEN')
        if condition:
            self.block()
            while self.current_token[0] != 'END' and self.current_token[0] != 'ELSE':
                self.eat(self.current_token[0])
        else:
            while self.current_token[0] != 'ELSE' and self.current_token[0] != 'END':
                self.eat(self.current_token[0])
            if self.current_token[0] == 'ELSE':
                self.eat('ELSE')
                self.block()
        self.eat('END')

    def while_statement(self):
        self.eat('WHILE')
        condition_index = self.current_token_index
        condition = self.boolean_expression()
        self.eat('DO')
        while condition:
            self.block()
            self.current_token_index = condition_index
            self.current_token = self.tokens[self.current_token_index]
            condition = self.boolean_expression()
            self.eat('DO')
        while self.current_token[0] != 'END':
            self.eat(self.current_token[0])
        self.eat('END')

    def boolean_expression(self):
        left = self.arithmetic_expression()
        operator = self.current_token[0]
        self.eat(operator)
        right = self.arithmetic_expression()
        return self.evaluate_boolean_expression(left, right, operator)

    def evaluate_boolean_expression(self, left, right, operator):
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
            self.error(f"Execution error: Unsupported operator {operator}")

    def arithmetic_expression(self):
        if self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            self.eat('ID')
            return self.variables.get(var_name, 0)  # Default to 0 if variable not found
        elif self.current_token[0] == 'LITERAL_INTEGER':
            value = int(self.current_token[1])
            self.eat('LITERAL_INTEGER')
            return value
        elif self.current_token[0] in ['ADD_OPERATOR', 'SUB_OPERATOR', 'MUL_OPERATOR', 'DIV_OPERATOR']:
            operator = self.current_token[0]
            self.eat(operator)
            left = self.arithmetic_expression()
            right = self.arithmetic_expression()
            return self.evaluate_expression(left, right, operator)
        else:
            self.error(f"Execution error: Unexpected token {self.current_token[0]} in arithmetic_expression")

    def evaluate_expression(self, left, right, operator):
        if operator == 'ADD_OPERATOR':
            return left + right
        elif operator == 'SUB_OPERATOR':
            return left - right
        elif operator == 'MUL_OPERATOR':
            return left * right
        elif operator == 'DIV_OPERATOR':
            if right == 0:
                self.error("Division by zero")
            return left / right
        else:
            self.error(f"Execution error: Unsupported operator {operator}")

# tokenize and interpret the code
tokens = tokenize(code)
interpreter = Interpreter(tokens)
interpreter.interpret()


