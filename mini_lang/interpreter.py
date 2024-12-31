class SimpleInterpreter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.symbol_table = {}  # Stores variable values
        self.labels = {}  # Stores label positions in the instruction list
        self.pc = 0  # Program counter
        self.last_cmp = None  # Stores the result of the last comparison

    def execute(self):
        # Preprocess labels
        self._preprocess_labels()
        
        # Execute instructions
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self._execute_instruction(instr)
            self.pc += 1

    def _preprocess_labels(self):
        """Preprocess labels to map them to instruction indices."""
        for idx, instr in enumerate(self.instructions):
            if instr.startswith("label"):
                _, label_name = instr.split(" ", 1)
                self.labels[label_name] = idx

    def _execute_instruction(self, instr):
        """Execute a single instruction."""
        parts = instr.split(" ", 1)
        operation = parts[0]
        args = parts[1].split(", ") if len(parts) > 1 else []

        if operation == "MOV":
            if args[1].isdigit():
                self.symbol_table[args[0]] = int(args[1])
            else:
                if args[1] in self.symbol_table:
                    self.symbol_table[args[0]] = self.symbol_table[args[1]]
                else:
                    self.symbol_table[args[0]] = 0
        elif operation == "ADD":
            self.symbol_table[args[0]] = self._get_value(args[1]) + self._get_value(args[2])
        elif operation == "SUB":
            self.symbol_table[args[0]] = self._get_value(args[1]) - self._get_value(args[2])
        elif operation == "CMP":
            self.last_cmp = self._get_value(args[0]) < self._get_value(args[1])
        elif operation == "JMP":
            self.pc = self.labels[args[0]] - 1  # Jump to the label
        elif operation == "PRINT":
            value = self.symbol_table.get(args[0], " ".join(args).strip('"'))
            print(value)
        elif operation.startswith("J"):  # Handle conditional jumps
            if operation == "JMP" or (operation == "JGE" and not self.last_cmp):
                self.pc = self.labels[args[0]] - 1
        elif operation.startswith("label"):
            pass  # Labels are just markers, nothing to execute
        elif operation == "WHILE":
            # Handle the while loop
            while self._get_value(args[0]) < self._get_value(args[1]):
                # Execute the body of the loop
                self.pc += 1  # Continue to the next instruction within the while loop
                self._execute_instruction(self.instructions[self.pc])
            # Exit the loop when condition fails
            return

    def _get_value(self, operand):
        """Return the value of an operand, which could be a variable or a literal number."""
        if operand.isdigit():
            return int(operand)
        return self.symbol_table.get(operand, 0)

    def get_symbol_table(self):
        return self.symbol_table


# Example usage
if __name__ == "__main__":
    from parser import parser
    from ir_generator import IRGenerator
    from optimizer import IROptimizer
    from code_gen import CodeGenerator

    data = '''
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    c = c - 5;
    print(c);
    if (c < 10) {
        print("c is less than 10");
    } else {
        print("c is greater than or equal to 10");
    }
    print(c);
    '''
    ast = parser.parse(data)
    ir_generator = IRGenerator()
    instructions = ir_generator.generate(ast)
    optimizer = IROptimizer()
    instructions = optimizer.optimize(instructions)
    code_gen = CodeGenerator()
    code_gen.generate_target_code(instructions)
    instructions = code_gen.get_generated_code().split("\n")

    print("Original Instructions:")
    for instr in instructions:
        print(instr)

    print("\nExecuting Instructions:")
    print("-" * 20)

    interpreter = SimpleInterpreter(instructions)
    interpreter.execute()
    print("-" * 20)

    # Show final values of variables
    print("Final Symbol Table:", interpreter.get_symbol_table())
