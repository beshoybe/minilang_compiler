import ply.yacc as yacc
from lexer import tokens  # Assuming lexer.py defines the tokens

symbol_table = {}

def add_variable_to_symbol_table(identifier, var_type):
    if identifier in symbol_table:
        raise Exception(f"Variable '{identifier}' is already declared.")
    symbol_table[identifier] = var_type

# AST node classes

class VariableDeclaration:
    def __init__(self, var_type, identifier, value):
        self.var_type = var_type  # Type of the variable (e.g., int, float, string)
        self.identifier = identifier  # Variable being declared
        self.value = value  # Value being assigned

    def __repr__(self):
        return f"VariableDeclaration({self.var_type}, {self.identifier}, {self.value})"

class AssignStatement:
    def __init__(self, identifier, value):
        self.identifier = identifier  # Variable being assigned
        self.value = value  # Value being assigned

    def __repr__(self):
        return f"AssignStatement({self.identifier}, {self.value})"

class IfStatement:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition  # The condition of the if statement
        self.body = body  # The body of the if statement (a list of statements)
        self.else_body = else_body  # Optional else body

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.body}, {self.else_body})"

class ReturnStatement:
    def __init__(self, value):
        self.value = value  # The expression to be returned

    def __repr__(self):
        return f"ReturnStatement({self.value})"

class PrintStatement:
    def __init__(self, value):
        self.value = value  # The expression to be printed

    def __repr__(self):
        return f"PrintStatement({self.value})"
class InputStatement:
    def __init__(self, value):
        self.value = value  # The expression to be input

    def __repr__(self):
        return f"InputStatement({self.value})"
class FunctionDefinition:
    def __init__(self, name, parameters, body, return_type):
        self.name = name  # The name of the function
        self.parameters = parameters  # A list of parameters
        self.body = body  # The body of the function (a list of statements)
        self.return_type = return_type  # The return type of the function

    def __repr__(self):
        return f"FunctionDefinition({self.name}, {self.parameters}, {self.body}, {self.return_type})"

class FunctionCall:
    def __init__(self, function_name, arguments):
        self.function_name = function_name  # The function being called
        self.arguments = arguments  # List of arguments being passed to the function

    def __repr__(self):
        return f"FunctionCall({self.function_name}, {self.arguments})"

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition  # The condition of the while loop
        self.body = body  # The body of the while loop (a list of statements)

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"

class Program:
    def __init__(self, statements):
        self.statements = statements  # List of statements (e.g., assignments)

    def __repr__(self):
        return f"Program({self.statements})"

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'GREATER', 'LESS', 'GREATEROREQUAL', 'LESSEQUAL', 'EQEQUAL', 'NEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


# Define the grammar for the parser

def p_program(p):
    '''program : statement
               | program statement'''
    if len(p) == 2:
        p[0] = Program([p[1]])
    else:
        p[0] = Program(p[1].statements + [p[2]])

# Handle variable declaration (with a type) and assignment
def p_statement_declaration(p):
    '''statement : type IDENTIFIER SEMICOLON
                 | type IDENTIFIER EQUAL expression SEMICOLON'''
    var_type = p[1]
    identifier = p[2]
    if identifier in symbol_table:
        raise Exception(f"Variable '{identifier}' is already declared.")
    add_variable_to_symbol_table(identifier, var_type)  # Add the variable to the symbol table

    if len(p) >4:
        p[0] = VariableDeclaration(p[1], p[2], p[4])
    else:
        p[0] = VariableDeclaration(p[1], p[2], None)


def p_statement_assign(p):
    '''statement : IDENTIFIER EQUAL expression SEMICOLON'''
    identifier = p[1]
    value = p[3]
    if identifier not in symbol_table:
        raise Exception(f"Variable '{identifier}' is not declared.")
    p[0] = AssignStatement(p[1], p[3])  # Assign a value to an existing variable


def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE program RBRACE
                | IF LPAREN expression RPAREN LBRACE program RBRACE ELSE LBRACE program RBRACE'''

    if len(p) == 12:  # Handling "if-else" statements
        p[0] = IfStatement(p[3], p[6], p[10])  # If with an optional else body
    else:  # Handling just "if"
        p[0] = IfStatement(p[3], p[6])  # If with no else body

def p_statement_return(p):
    '''statement : RETURN expression SEMICOLON'''
    p[0] = ReturnStatement(p[2])  # Create a ReturnStatement with the return expression

def p_statement_print(p):
    '''statement : PRINT expression SEMICOLON'''
    p[0] = PrintStatement(p[2])  # Create a PrintStatement with the expression to be printed

def p_satement_input(p):
    '''statement : INPUT expression SEMICOLON'''
    p[0] = InputStatement(p[2])

# Function definition
def p_statement_function(p):
    '''statement : type FUNCTION IDENTIFIER LPAREN params RPAREN LBRACE program RBRACE'''

    p[0] = FunctionDefinition(p[3], p[5], p[8], p[1])  # Create a FunctionDefinition with name, parameters, and body

def p_params_empty(p):
    '''params : '''
    p[0] = []  # No parameters

def p_params(p):
    '''params : type IDENTIFIER
              | params COMMA type IDENTIFIER'''
    if len(p) == 3:
        p[0] = [p[1], p[2]] # Single parameter
    else:
        p[0] = [p[1]] + [[p[3], p[4]]]  # Add a new parameter

# Function call
def p_statement_function_call(p):
    '''statement : IDENTIFIER LPAREN args RPAREN SEMICOLON'''
    p[0] = FunctionCall(p[1], p[3])  # Function call as a statement

# Expression for function call
def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN args RPAREN'''
    p[0] = FunctionCall(p[1], p[3])  # Function call as an expression

def p_args_empty(p):
    '''args : '''
    p[0] = []  # No arguments

def p_args(p):
    '''args : expression
            | args COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Logical expressions
def p_expression_logical_or(p):
    '''expression : expression OR expression'''
    p[0] = (p[1], '||', p[3])

def p_expression_logical_and(p):
    '''expression : expression AND expression'''
    p[0] = (p[1], '&&', p[3])

# Comparison expressions
def p_expression_comparison(p):
    '''expression : expression GREATER expression
                  | expression LESS expression
                  | expression GREATEROREQUAL expression
                  | expression LESSEQUAL expression
                  | expression EQEQUAL expression
                  | expression NEQUAL expression'''
    p[0] = (p[1], p[2], p[3])

# Arithmetic expressions
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[1], p[2], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = float(p[1])  # Convert number to float

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1]

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = p[1]

def p_expression_true(p):
    '''expression : TRUE'''
    p[0] = True

def p_expression_false(p):
    '''expression : FALSE'''
    p[0] = False

# Rule for handling parentheses (for grouping expressions)
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]  # Return the expression inside the parentheses

# While statement
def p_statement_while(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE program RBRACE'''
    p[0] = WhileStatement(p[3], p[6])  # Create a WhileStatement with condition and body

# Type (for variable declarations)
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL
            | STR
            '''
    p[0] = p[1]  # Return the type name (e.g., "int", "float", "bool")

# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test the parser with variable declaration (with type)
if __name__ == '__main__':
    data = '''
    int b;
    int x = 5;
    b = 10;
    float y = 3.14;
    bool z = true;
    str s = "hello";
    int function add(int a,int b) {
        int nn = a + b;
        return nn;
    }
    add(1, 2);
    int function sub(float f){
        print("Hello");
        }
    
    while (x < y) {
        print(x);
        x = x + 1;
    }
    
    if (x > y) {
        print("x is greater");
    } else {

        print("y is greater");
    }
    x = add(1, 3);
    
    print(x);
    print(z);
    input(b);
    '''
    print("Parsing input...")
    ast = parser.parse(data)
    print("Parsed AST:", ast)
