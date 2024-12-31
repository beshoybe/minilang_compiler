from ir_generator import IRInstruction

class IROptimizer:
    def __init__(self):
        self.optimized_instructions = []
        self.variable_values = {}  # Keeps track of variable values (for constant folding)

    def optimize(self, instructions):
        """Optimize the given list of instructions."""
        self.optimized_instructions = []
        for instruction in instructions:
            self.optimize_instruction(instruction)
        return self.optimized_instructions

    def optimize_instruction(self, instruction):
        """Optimize individual instruction."""
        # Apply constant folding
        if instruction.op in ('+', '-', '*', '/'):
            # Check if both arguments are constants
            left = self.evaluate_operand(instruction.args[0])
            right = self.evaluate_operand(instruction.args[1])

            if left is not None and right is not None:
                # Perform the constant folding
                result = self.evaluate_operation(instruction.op, left, right)
                # Replace the operation with the constant result
                temp_var = self.get_temp_variable()
                self.optimized_instructions.append(IRInstruction('=', temp_var, result))
                return  # Skip adding the original instruction

        # Handle dead code elimination (e.g., x = x is redundant)
        if instruction.op == '=' and instruction.args[0] == instruction.args[1]:
            # Remove redundant assignments
            return

        # Handle assignments that can be simplified (e.g., assignment to a variable that's already known)
        if instruction.op == '=':
            # Check if the variable already has a known value
            if instruction.args[1] in self.variable_values:
                # If the value is already known, replace the assignment
                self.optimized_instructions.append(IRInstruction('=', instruction.args[0], self.variable_values[instruction.args[1]]))
                return
            else:
                # Otherwise, track the variable value
                self.variable_values[instruction.args[0]] = instruction.args[1]

        # If instruction produces a result, add it to the optimized instructions
        self.optimized_instructions.append(instruction)

    def evaluate_operand(self, operand):
        """Evaluate if the operand is a constant value."""
        # Check if the operand is a number (constant)
        if isinstance(operand, (int, float)):
            return operand
        # If operand is a variable, check if its value is already known
        if operand in self.variable_values:
            return self.variable_values[operand]
        return None  # Not a constant

    def evaluate_operation(self, op, left, right):
        """Perform the arithmetic operation."""
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        return None

    def get_temp_variable(self):
        """Generate a new temporary variable for optimizations."""
        return f"t{len(self.optimized_instructions)}"


# Example Usage
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
    int d = add(1, 2);
    print(d);

'''
    from parser import parser
    from ir_generator import IRGenerator
    ast = parser.parse(data)
    ir_generator = IRGenerator()
    instructions = ir_generator.generate(ast)
    print("Original Instructions:")
    for instr in instructions:
        print(instr)
    # Optimize the instructions
    optimizer = IROptimizer()
    optimized_instructions = optimizer.optimize(instructions)
    
    print("Optimized Instructions:")
    for instr in optimized_instructions:
        print(instr)
