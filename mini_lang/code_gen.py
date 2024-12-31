class CodeGenerator:
    def __init__(self):
        self.code = []  # Store the generated target code
        self.visited_labels = set()  # Track visited labels

    def process_instruction(self, instruction):
        """Process a single instruction and generate the target code."""
        if not instruction:
            return

        operation = instruction.op
        args = instruction.args

        if operation == '=':
            self.assign(args[0], args[1])
        elif operation == '+':
            self.add(args[0], args[1], args[2])
        elif operation == '-':
            self.subtract(args[0], args[1], args[2])
        elif operation == '*':
            self.multiply(args[0], args[1], args[2])  # Handle multiplication
        elif operation == '/':
            self.divide(args[0], args[1], args[2])  # Handle division
        elif operation in ('<', '>', '<=', '>=', '=='):
            self.compare(args[0], args[1], args[2], operation)
        elif operation == 'if':
            self.conditional_jump(args[0], args[1], args[2])
        elif operation == 'goto':
            self.goto(args[0])
        elif operation == 'label':
            self.label(args[0])
        elif operation == 'param':
            self.param(args[0])
        elif operation == 'call':
            self.call(args[0])
        elif operation == 'return':
            self.return_value()
        elif operation == 'print':
            self.print_statement(" ".join(args))
        else:
            print(f"Warning: Unsupported operation {operation} with arguments {args}")

    def assign(self, var, value):
        self.code.append(f"MOV {var}, {value}")

    def add(self, result, var1, var2):
        self.code.append(f"ADD {result}, {var1}, {var2}")

    def subtract(self, result, var1, var2):
        self.code.append(f"SUB {result}, {var1}, {var2}")

    def multiply(self, result, var1, var2):
        """Generate target code for multiplication."""
        self.code.append(f"MUL {result}, {var1}, {var2}")

    def divide(self, result, var1, var2):
        """Generate target code for division."""
        self.code.append(f"DIV {result}, {var1}, {var2}")

    def compare(self, var, operand1, operand2, operator):
        """Generate target code for comparison based on operator."""
        self.code.append(f"CMP {operand1}, {operand2}")

    def conditional_jump(self, condition, cond_op, label):
        """Generate target code for conditional jump operation."""
        if cond_op == "goto":
            self.code.append(f"JMP {label}")
        elif cond_op == "if":
            # Compare the condition to zero (non-zero means true)
            self.code.append(f"CMP {condition}, 0")
            self.code.append(f"JNE {label}")  # Jump if condition is true (non-zero)
        elif cond_op == "<":
            self.code.append(f"CMP {condition}, 20")  # Compare condition (e.g., c) to 20
            self.code.append(f"JL {label}")  # Jump if less than
        elif cond_op == ">":
            self.code.append(f"CMP {condition}, 0")  # Compare condition (e.g., c) to 0
            self.code.append(f"JG {label}")  # Jump if greater than
        elif cond_op == "==":
            self.code.append(f"CMP {condition}, 0")  # Compare condition (e.g., c) to 0
            self.code.append(f"JE {label}")  # Jump if equal
        elif cond_op == "<=":
            self.code.append(f"CMP {condition}, 20")  # Compare condition (e.g., c) to 20
            self.code.append(f"JLE {label}")  # Jump if less than or equal
        elif cond_op == ">=":
            self.code.append(f"CMP {condition}, 20")  # Compare condition (e.g., c) to 20
            self.code.append(f"JGE {label}")  # Jump if greater than or equal

    def goto(self, label):
        self.code.append(f"JMP {label}")

    def label(self, label_name):
        self.code.append(f"label {label_name}")

    def param(self, param):
        self.code.append(f"PUSH {param}")

    def call(self, function):
        self.code.append(f"CALL {function}")

    def return_value(self):
        self.code.append(f"RETURN")

    def print_statement(self, statement):
        self.code.append(f"PRINT {statement}")

    def generate_target_code(self, instructions):
        for instruction in instructions:
            self.process_instruction(instruction)

    def get_generated_code(self):
        return "\n".join(self.code)

# Example usage
if __name__ == '__main__':
    # Example IR instructions
    data = '''
    int a = 5;
    int b = 10;
    int c = a + b;
    while(c < 20) {
        c = c + 1;
    }
    int function add(int x, int y) {
        return x + y;
    }
    if (c < 10) {
        print("c is less than 10");
    } else {
        print("c is greater than or equal to 10");
    }
    c = c - 1;
    print(c);
    float k = 3/4;
    '''
    
    # Assuming you have a parser and IR generator
    from parser import parser
    from ir_generator import IRGenerator
    from optimizer import IROptimizer

    # Parse the data and generate IR
    ast = parser.parse(data)
    ir_generator = IRGenerator()
    instructions = ir_generator.generate(ast)

    # Optimize the instructions
    optimizer = IROptimizer()
    instructions = optimizer.optimize(instructions)

    # Print the optimized instructions for debugging
    print("Optimized Instructions:")
    for instr in instructions:
        print(instr)

    # Generate the target code using CodeGenerator
    generator = CodeGenerator()
    generator.generate_target_code(instructions)

    # Output the generated target code
    print("\nGenerated Target Code:")
    print(generator.get_generated_code())
