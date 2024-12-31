from parser import parser, Program, VariableDeclaration, AssignStatement, IfStatement, ReturnStatement, PrintStatement, InputStatement, FunctionDefinition, FunctionCall, WhileStatement
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.symbol_value = {}
        self.functions = {}

    def add_variable(self, identifier, var_type,var_value=None):
        if identifier in self.symbol_table:
            raise Exception(f"Variable '{identifier}' is already declared.")
        self.symbol_table[identifier] = var_type
        if var_value:
            self.symbol_value[identifier] = var_value

    def get_variable_type(self, identifier):
        if identifier not in self.symbol_table:
            raise Exception(f"Variable '{identifier}' is not declared.")
        return self.symbol_table[identifier]

    def add_function(self, function_name, return_type, parameters):
        if function_name in self.functions:
            raise Exception(f"Function '{function_name}' is already declared.")
        self.functions[function_name] = {'return_type': return_type, 'parameters': parameters}

    def get_function(self, function_name):
        if function_name not in self.functions:
            raise Exception(f"Function '{function_name}' is not declared.")
        return self.functions[function_name]

    def check_type(self, left, right, operator):
        # Ensure both operands are of compatible types

        if left == right and left in ('int', 'float', 'bool'):
            if operator in ('+', '-', '*', '/'):
                return left
            else:
                return 'bool'
        elif left == 'int' and right == 'float':
            if operator in ('+', '-', '*', '/'):
                return 'float'
            else:
                return 'bool'
        elif left == 'float' and right == 'int':
            if operator in ('+', '-', '*', '/'):
                return 'float'
            else:
                return 'bool'
        
        else:
            raise Exception(f"Type mismatch: cannot apply '{operator}' to '{left}' and '{right}'.")


    def analyze(self, node,parent=None):

        if isinstance(node, Program):
            for statement in node.statements:
                self.analyze(statement)

        elif isinstance(node, VariableDeclaration):
            # Add variable to the symbol table
            self.add_variable(node.identifier, node.var_type,node.value)

            if node.value:
                value_type = self.analyze(node.value,parent=parent)
                if value_type != node.var_type:
                    raise Exception(f"Type mismatch: '{node.identifier}' declared as {node.var_type} but assigned {value_type}.")
            return node.var_type

        elif isinstance(node, AssignStatement):
            # Ensure the variable is declared
            var_type = self.get_variable_type(node.identifier)
            value_type = self.analyze(node.value)
            if var_type != value_type:
                raise Exception(f"Type mismatch: cannot assign {value_type} to variable '{node.identifier}' of type {var_type}.")
            self.symbol_value[node.identifier] = node.value
            return var_type

        elif isinstance(node, IfStatement):
            # Check condition type (should be a boolean)
            condition_type = self.analyze(node.condition)
            if condition_type != 'bool':
                raise Exception(f"Type mismatch: condition in 'if' statement should be of type 'bool', got {condition_type}.")
            # Check the body of the if statement
            for stmt in node.body.statements:
                self.analyze(stmt)
            if node.else_body:
                for stmt in node.else_body.statements:
                    self.analyze(stmt)

        elif isinstance(node, ReturnStatement):
            # Ensure return type matches the function's return type
            if self.check_is_global_variable(node.value):
                return_type = self.get_variable_type(node.value)
            else:
                return_type = self.analyze(node.value)
            if parent.return_type != return_type:
                
                raise Exception(f"Type mismatch: function '{parent.name}' expects return type {parent.return_type}, got {return_type}.")
            return return_type

        elif isinstance(node, PrintStatement):
            # Ensure print argument is valid
            self.analyze(node.value)

        elif isinstance(node, InputStatement):
            # Input can be any type
            return self.analyze(node.value)

        elif isinstance(node, FunctionDefinition):
            # Add function to the function table
            self.add_function(node.name, node.return_type, node.parameters)
            has_return = False
            # Analyze function body
            for stmt in node.body.statements:
                if isinstance(stmt, ReturnStatement):
                    has_return = True
                self.analyze(stmt, parent=node)
            if not has_return:
                raise Exception(f"Function '{node.name}' is missing a return statement.")

        elif isinstance(node, FunctionCall):
            # Ensure the function is defined
            func_info = self.get_function(node.function_name)
            if len(node.arguments) != len(func_info['parameters']):
                raise Exception(f"Function '{node.function_name}' expects {len(func_info['parameters'])} arguments, got {len(node.arguments)}.")
            for arg, param in zip(node.arguments, func_info['parameters']):
                arg_type = self.analyze(arg)
                if arg_type != param[0]:
                    raise Exception(f"Argument type mismatch: expected {param}, got {arg_type} for '{arg}' in function '{node.function_name}'.")

            return func_info['return_type']

        elif isinstance(node, WhileStatement):
            # Check condition type (should be a boolean)
            condition = node.condition
            new_condition = []
            for con in condition:
                if self.check_is_global_variable(con):
                    new_condition.append(self.get_variable_value(con))
                else:
                    new_condition.append(con)
            new_condition = tuple(new_condition)
            condition_type = self.analyze(new_condition)
            if condition_type != 'bool':
                raise Exception(f"Type mismatch: condition in 'while' statement should be of type 'bool', got {condition_type}.")
            for stmt in node.body.statements:
                self.analyze(stmt)

        elif isinstance(node, tuple):  # for expressions like ('x', '+', 'y')
            left_type = self.analyze(node[0])
            right_type = self.analyze(node[2])
            left_value = node[0]
            right_value = node[2]
            is_function = parent and isinstance(parent, FunctionDefinition)
            is_left_global = self.check_is_global_variable(left_value)
            is_right_global = self.check_is_global_variable(right_value)
            params = parent.parameters if is_function else None
            
            if is_function:
                for i in range(len(params)):
                    if params[i][1] == left_value:
                        left_type = params[i][0]
                    if params[i][1] == right_value:
                        right_type = params[i][0]
            if is_left_global:
                left_type = self.get_variable_type(left_value)
            if is_right_global:
                right_type = self.get_variable_type(right_value)
            return self.check_type(left_type, right_type, node[1])
        

        elif isinstance(node, (int, float, bool, str)):
            #remove zero from float
            if isinstance(node, float) and node.is_integer():
                return 'int'
            # Literal values return their respective type
            return type(node).__name__

        elif isinstance(node, str):  # Variable reference
            return self.get_variable_type(node)

        else:
            raise Exception(f"Unknown node type: {type(node)}")
        
    def check_is_global_variable(self,identifier):
        if identifier in self.symbol_table:
            return True
        return False
    def get_variable_value(self,identifier):
        return self.symbol_value[identifier]

# Example of running the semantic analysis
if __name__ == '__main__':
    analyzer = SemanticAnalyzer()
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
        int function sub(){
            print("Hello");
            return 1;
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
    # Assume the parser has already been run and the AST is stored in `ast`
    ast = parser.parse(data)
    try:
        analyzer.analyze(ast)
        print("Semantic analysis passed!")
    except Exception as e:
        print(f"Semantic analysis failed: {e}")
        #print stack trace
        import traceback
        traceback.print_exc()