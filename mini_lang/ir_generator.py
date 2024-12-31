from parser import Program, VariableDeclaration, AssignStatement, FunctionDefinition, ReturnStatement, WhileStatement, IfStatement

class IRInstruction:
    def __init__(self, op, *args):
        self.op = op  # Operation type (e.g., '=', 'call', 'jump')
        self.args = args  # Arguments for the operation (can be multiple)

    def __repr__(self):
        # Represent the instruction in a readable format (correct TAC format)
        return f"{self.op} {' '.join(map(str, self.args))}"

class IRGenerator:
    def __init__(self):
        self.instructions = []  # Store generated IR instructions
        self.temp_counter = 0   # Counter for temporary variables
        self.label_counter = 0  # Counter for labels

    def generate(self, ast):
        """Start generating IR from the AST."""
        self.visit(ast)
        return self.instructions

    def visit(self, node):
        """Dispatch to the appropriate visitor method."""
        if isinstance(node, (int, float)):
            return self.visit_number(node)
        elif isinstance(node, str):  # Handle strings here
            return self.visit_string(node)
        elif isinstance(node, tuple):
            return self.visit_tuple(node)  # Handle binary expressions as tuples
        elif isinstance(node, WhileStatement):
            return self.visit_WhileStatement(node)
        elif isinstance(node, IfStatement):
            return self.visit_IfStatement(node)  # Handle if-else
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(f"Unknown node type: {type(node)}")  # Log the unknown node type
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Program(self, node):
        """Visit each statement in the program."""
        if not hasattr(node, 'statements'):
            raise ValueError(f"Program node should have 'statements' attribute, got {type(node)}")
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDeclaration(self, node):
        """Handle variable declaration with a possible missing value."""
        if node.value is None:
            if node.var_type == 'int':
                value = 0
            elif node.var_type == 'float':
                value = 0.0
            elif node.var_type == 'bool':
                value = 'false'
            elif node.var_type == 'str':
                value = '""'  # Empty string
            else:
                value = None  # Default case, might need more handling
        else:
            value = self.visit(node.value)

        temp = self.get_temp_variable()
        self.instructions.append(IRInstruction('=', temp, value))  # t1 = value (temporary assignment)
        self.instructions.append(IRInstruction('=', node.identifier, temp))  # x = t1 (assign temp to variable)

    def visit_AssignStatement(self, node):
        """Handle assignment statements."""
        value = self.visit(node.value)  # Visit the assigned value (expression)
        self.instructions.append(IRInstruction('=', node.identifier, value))  # x = value (assignment to variable)

    def visit_FunctionDefinition(self, node):
        """Handle function definition and generate its IR."""
        if not hasattr(node, 'body') or not hasattr(node.body, 'statements'):
            raise ValueError(f"Function definition is missing a valid body with 'statements'. Got {type(node.body)}")

        function_label = self.get_function_label(node.name)
        end_function_label = f"end_{function_label}"  # Create end label for the function

        # Function entry label
        self.instructions.append(IRInstruction('label', function_label))  # Label for function entry

        # Handle parameters as local variables
        for idx, param in enumerate(node.parameters):
            param_name = param[1]  # Extract parameter name
            self.instructions.append(IRInstruction('param', param_name))  # Generate parameter IR
        
        # Visit the function body
        for statement in node.body.statements:
            if isinstance(statement, ReturnStatement):
                return_stmt = statement
                return_value = self.visit(return_stmt.value)
                self.instructions.append(IRInstruction('return', return_value))  # return value from function
            else:
                self.visit(statement)

        # Function exit label
        self.instructions.append(IRInstruction('label', end_function_label))  # Label for function exit

    def visit_ReturnStatement(self, node):
        """Handle return statements."""
        return self.visit(node.value)

    def visit_tuple(self, node):
        """Handle binary expressions represented as tuples (e.g., ('a', '+', 'b'))."""
        left = self.visit(node[0])  # Left operand (e.g., 'a')
        operator = node[1]  # Operator (e.g., '+')
        right = self.visit(node[2])  # Right operand (e.g., 'b')

        # Generate a temporary variable for the result
        temp = self.get_temp_variable()
        self.instructions.append(IRInstruction(operator, temp, left, right))  # t1 = left operator right
        return temp  # Return the temporary variable holding the result

    def visit_number(self, node):
        """Handle both integers and floats."""
        if isinstance(node, float) and node.is_integer():
            return str(int(node))  
        if isinstance(node, float):  # If it's a float, format it
            return f"{node:.6f}"  # Represent float in TAC with precision
        elif isinstance(node, int):  # If it's an integer
            return str(node)  # Return integer as it is
        return str(node)  # Otherwise, treat it as an identifier (string)

    def visit_string(self, node):
        """Handle string literals."""
        return f'{node}'  # Return the string with proper quotes for TAC

    def get_temp_variable(self):
        """Generate a new temporary variable."""
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def get_function_label(self, function_name):
        """Generate a unique label for the function."""
        return f"func_{function_name}"

    def visit_FunctionCall(self, node):
        """Handle function calls."""
        if node.function_name == 'print':
            self.instructions.append(IRInstruction('print', self.visit(node.arguments[0])))
            return

        for idx, arg in enumerate(node.arguments):
            self.instructions.append(IRInstruction('param', self.visit(arg)))  # Pass arguments as parameters
        
        function_label = self.get_function_label(node.function_name)
        temp_var = self.get_temp_variable()  # Generate a temporary variable for the return value
        self.instructions.append(IRInstruction('call', function_label))  # Call the function
        self.instructions.append(IRInstruction('=', temp_var, 'return_value'))  # Capture return value

        return temp_var  # Return the temporary variable that holds the return value


    def visit_PrintStatement(self, node):
        """Handle print statements."""
        self.instructions.append(IRInstruction('print', self.visit(node.value)))

    def visit_WhileStatement(self, node):
        """Handle while loop statements."""
        start_label = self.get_label()
        end_label = self.get_label()

        self.instructions.append(IRInstruction('label', start_label))
        condition = self.visit(node.condition)
        self.instructions.append(IRInstruction('if', condition, 'goto', end_label))

        for statement in node.body.statements:
            self.visit(statement)

        self.instructions.append(IRInstruction('goto', start_label))
        self.instructions.append(IRInstruction('label', end_label))

    def visit_IfStatement(self, node):
        """Handle if-else statements."""
        # Generate labels for the if-else branches
        else_label = self.get_label()
        end_label = self.get_label()

        # Evaluate the condition of the if statement
        condition = self.visit(node.condition)
        self.instructions.append(IRInstruction('if', condition, 'goto', else_label))  # If condition is false, jump to else

        # Visit the if-block
        for statement in node.body.statements:
            self.visit(statement)

        # After the if-block, jump to the end of the if-else
        self.instructions.append(IRInstruction('goto', end_label))

        # Handle the else-block if present
        if node.else_body:  # Check if else_body exists
            self.instructions.append(IRInstruction('label', else_label))
            for statement in node.else_body.statements:
                self.visit(statement)

        # End of if-else block
        self.instructions.append(IRInstruction('label', end_label))

    def get_label(self):
        """Generate a new label."""
        self.label_counter += 1
        return f"label_{self.label_counter}"

if __name__=='__main__':
    # Example AST input (from your example)
    data = '''
    int x;
    float y = 3.14;
    bool z = true;
    str s = "hello";
    x = 5;
    x = x-1;
    int function add(int a, int b) {
        return a + b;
    }
    int f = add(1, 2);
    int function sub() {
        print("Hello");
        return 1;
    }
    sub();
    while (x < 10) {
        print(x);
        x = x + 1;
    }
    if (x == 10) {
        print(x);
    }
    '''
    from parser import parser
    ast = parser.parse(data)
    ir_generator = IRGenerator()
    ir_instructions = ir_generator.generate(ast)
    print(ir_instructions)
