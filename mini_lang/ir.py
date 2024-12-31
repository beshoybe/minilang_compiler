class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.code = []

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate_tac(self, ast):
        for node in ast:
            if node[0] == 'function':
                self.generate_function(node)
            elif node[0] == 'while':
                self.generate_while(node)

    def generate_function(self, node):
        function_name = node[1]
        params = node[2]
        body = node[3]
        self.code.append(f"Function {function_name}:")
        for stmt in body:
            self.generate_statement(stmt)

    def generate_statement(self, stmt):
        if stmt[0] == 'assignment':
            self.generate_assignment(stmt)
        elif stmt[0] == 'return':
            self.generate_return(stmt)
        elif stmt[0] == 'while':
            self.generate_while(stmt)

    def generate_assignment(self, stmt):
        var = stmt[1]
        expr = stmt[2]
        if expr[0] == 'number':
            self.code.append(f"{var} = {expr[1]}")
        elif expr[0] == 'identifier':
            self.code.append(f"{var} = {expr[1]}")
        elif expr[0] == '+':
            temp = self.new_temp()
            self.code.append(f"{temp} = {expr[1][1]} + {expr[2][1]}")
            self.code.append(f"{var} = {temp}")
        elif expr[0] == '-':
            temp = self.new_temp()
            self.code.append(f"{temp} = {expr[1][1]} - {expr[2][1]}")
            self.code.append(f"{var} = {temp}")

    def generate_return(self, stmt):
        expr = stmt[1]
        if expr[0] == '+':
            temp = self.new_temp()
            self.code.append(f"{temp} = {expr[1][1]} + {expr[2][1]}")
            self.code.append(f"return {temp}")
        elif expr[0] == 'identifier':
            self.code.append(f"return {expr[1]}")

    def generate_while(self, stmt):
        condition = stmt[1]
        body = stmt[2]
        start_label = self.new_temp()  # Unique label for start of the loop
        end_label = self.new_temp()    # Unique label for end of the loop

        # Start of the while loop
        self.code.append(f"{start_label}:")

        # Handling the condition: if x > y, continue; else, jump to the end
        if condition[0] == '>':
            temp_condition = self.new_temp()  # Temporary variable to hold the result of x - y
            self.code.append(f"{temp_condition} = {condition[1][1]} - {condition[2][1]}")  # x - y
            self.code.append(f"if {temp_condition} <= 0 goto {end_label}")  # If x <= y, exit the loop

        # Process the body of the while loop
        for s in body:
            self.generate_statement(s)

        # Jump back to the start of the loop if the condition is true
        self.code.append(f"goto {start_label}")

        # End of the while loop
        self.code.append(f"{end_label}:")

    def print_code(self):
        for line in self.code:
            print(line)

# Example usage:
tac_generator = TACGenerator()
from parser import parser
data = '''
function add(a, b) {
    return a + b;
}

function main(){
    x = 5;
    y = 2;
    z = add(x, y);
    while (x > y) {
        x = x - 1;
    }
}
'''
ast = parser.parse(data)

tac_generator.generate_tac(ast)
tac_generator.print_code()
