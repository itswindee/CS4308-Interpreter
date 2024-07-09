"""
 * Class:       CS 4308 Section W01
 * Term:        Summer 2024
 * Name:        Emily Zhu
 * Instructor:  Sharon Perry
 * Project:     Deliverable P1 Scanner
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

# token patterns for the lexical analyzer
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

grammar_rules = {
    'program': ['function'],
    'function': ['FUNCTION ID OPEN_PARENTHESIS CLOSE_PARENTHESIS block END'],
    'block': ['statement', 'block statement'],
    # Add more rules for statements, expressions, etc.
}

# Define a recursive descent parser
def parse(tokens, rule):
    if not tokens:
        return False
    for option in grammar_rules[rule]:
        remaining_tokens = tokens.copy()
        for token in option.split():
            if not remaining_tokens or remaining_tokens[0][0] != token:
                break
            remaining_tokens.pop(0)
        else:
            return True
    return False

# Test the parser with the given tokens
tokens = tokenize(code)
if parse(tokens, 'program'):
    print("The code follows the grammar rules.")
else:
    print("The code does not follow the grammar rules.")

