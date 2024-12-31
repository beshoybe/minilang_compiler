import ply.lex as lex

# List of reserved keywords
reserved = {
    'function': 'FUNCTION',
    'true': 'TRUE',
    'false': 'FALSE',
    'return': 'RETURN',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'input': 'INPUT',
    'int': 'INT',    # Added integer type keyword
    'float': 'FLOAT',  # Added float type keyword
    'bool': 'BOOL',    # Added boolean type keyword
    'str': 'STR'    # Added string type keyword
}

# List of token names
tokens = (
    'IDENTIFIER', 'NUMBER', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUAL', 'GREATER',
    'LESSEQUAL', 'LESS', 'EQEQUAL', 'NEQUAL', 'GREATEROREQUAL', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA', 'AND', 'OR',
    'COMMENT_SINGLE', 'COMMENT_MULTI'
) + tuple(reserved.values())

# Regular expressions for the tokens
t_FUNCTION = r'function'
t_NUMBER = r'\d+\.\d+|\d+'  # Matches floating-point and integer numbers
t_STRING = r'"([^\\"]|\\[nt"\\])*"'  # Matches strings with escape sequences
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_GREATER = r'>'  # Greater than
t_LESSEQUAL = r'<='  # Less than or equal to
t_LESS = r'<'
t_EQEQUAL = r'=='  # Equality operator
t_NEQUAL = r'!='  # Not equal to operator
t_GREATEROREQUAL = r'>='  # Greater than or equal to operator
t_AND = r'&&'  # Logical AND
t_OR = r'\|\|'  # Logical OR
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','

# Handle keywords
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check if the identifier is a reserved keyword
    return t

# Handle type keywords for variable declarations (int, float, bool)
def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_BOOL(t):
    r'bool'
    return t
def t_STR(t):
    r'str'
# A function to handle ignored characters like spaces and tabs
t_ignore = ' \t'

# Ignore comments by skipping them
def t_COMMENTSINGLE(t):
    r'//.*'
    pass  # Simply ignore single-line comments

def t_COMMENTMULTI(t):
    r'/\*[\s\S]*?\*/'
    pass  # Simply ignore multi-line comments

# Newline handling
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling with line and column reporting
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, column {t.lexpos}")
    t.lexer.skip(1)

# Input source code
data = '''
// This is a single-line comment
/* This is a 
multi-line comment */
int x = 10;
float y = 3.14;
bool z = true;
str s = "hello";
function add(a, b) {
    // Adding two numbers
    return a + b;
}

f = "hello";
x = true;
y = 3.14;
z = 10;
function main(){
    x = 5;
    y = 2;
    z = add(x, y);
    while (x >= y) {
        x = x - 1;
    }
    if (x != 0) {
        print("Done");
    } else {
        print("Not Done");
    }
}
'''

# Create the lexer
lexer = lex.lex()

if __name__ == '__main__':
    # Give the lexer the input data
    lexer.input(data)

    # Tokenize the input data
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
