# MiniLang Compiler Project

This project involves building a simple compiler for the language **MiniLang**. The compiler will go through multiple stages of compilation, including lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, and target code generation.

## Project Objectives

1. Understand the fundamental concepts of compiler construction.
2. Implement key components of a compiler pipeline.
3. Gain practical experience with Python for building complex software systems.
4. Develop debugging, testing, and optimization skills for software projects.

This project provides a simple framework for generating and optimizing intermediate representation (IR) instructions, simulating their execution, and generating target assembly-like code. It consists of several modules that work together to parse a high-level language, optimize the generated IR, generate assembly-like target code, and execute it through an interpreter.

## Features

- **IR Instruction Generation**: Convert high-level code into intermediate representation (IR) instructions.
- **Lexer and Parser**: Tokenize and parse high-level source code into an abstract syntax tree (AST).
- **Instruction Optimization**: Optimize the IR using common techniques such as constant folding and dead code elimination.
- **Target Code Generation**: Translate the optimized IR into target assembly-like code.
- **Simple Interpreter**: Simulate the execution of the generated target code by interpreting the instructions step by step.
- **Customizable**: Easily extend the functionality with more operations or optimizations.

## Project Structure

```
IR-Code-Generation/
│
├── lexer.py                # Lexical analysis of source code (tokenizer)
├── parser.py               # Parses the tokenized input into an AST
├── ir_generator.py         # Generates IR instructions from parsed code
├── optimizer.py            # Optimizes IR instructions
├── code_gen.py             # Generates target code (assembly-like)
├── interpreter.py          # Interprets the generated target code
├── main.py                 # Main file to run the pipeline (parsing, optimization, code generation, execution)
└── README.md               # This documentation
```

## Requirements

- Python 3.x
- No external libraries are required, but the project could be extended with libraries like `ply` for parsing or `numba` for JIT compilation.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/IR-Code-Generation.git
   cd IR-Code-Generation
   ```

2. No dependencies are required. You can run the scripts directly with Python 3.

## Usage

### 1. Lexer

The **lexer** (also known as tokenizer) is responsible for breaking down the input source code into tokens. Each token represents a basic building block of the language (like keywords, identifiers, operators, and literals).

In the current setup, `lexer.py` implements the lexical analysis. It reads a string of high-level code and returns a list of tokens that can be processed by the parser.

Example usage:

```python
from lexer import Lexer

source_code = '''
int a = 5;
int b = 10;
int c = a + b;
'''

lexer = Lexer()
tokens = lexer.tokenize(source_code)

# Print the generated tokens
for token in tokens:
    print(token)
```

### 2. Parser

The **parser** takes the list of tokens produced by the lexer and builds an **abstract syntax tree (AST)**. The AST represents the hierarchical structure of the program, which is then used for generating IR instructions.

`parser.py` is responsible for parsing the tokens into an AST.

Example usage:

```python
from parser import Parser
from lexer import Lexer

source_code = '''
int a = 5;
int b = 10;
int c = a + b;
'''

# Tokenize the source code
lexer = Lexer()
tokens = lexer.tokenize(source_code)

# Parse the tokens into an AST
parser = Parser()
ast = parser.parse(tokens)

# Print the generated AST
print(ast)
```

### 3. IR Instruction Generation

The `IRGenerator` module generates intermediate representation (IR) instructions from the parsed AST.

Example usage:

```python
from ir_generator import IRGenerator

# Generate IR instructions from the AST
ir_generator = IRGenerator()
instructions = ir_generator.generate(ast)

# Print the generated IR instructions
for instr in instructions:
    print(instr)
```

### 4. Optimizing IR Instructions

You can optimize the IR instructions using the `IROptimizer` module. This includes operations like constant folding and dead code elimination:

```python
from optimizer import IROptimizer

# Optimize the IR instructions
optimizer = IROptimizer()
optimized_instructions = optimizer.optimize(instructions)

# Print the optimized instructions
for instr in optimized_instructions:
    print(instr)
```

### 5. Generating Target Code

You can generate assembly-like target code using the `CodeGenerator` module:

```python
from code_gen import CodeGenerator

# Generate target code from optimized IR instructions
generator = CodeGenerator()
generator.generate_target_code(optimized_instructions)

# Print the generated target code
print(generator.get_generated_code())
```

### 6. Executing the Generated Code

You can use the `SimpleInterpreter` class to simulate the execution of the target code:

```python
from interpreter import SimpleInterpreter

# Assuming target code is generated by CodeGenerator
instructions = generator.get_generated_code().split("
")

# Create an interpreter and execute the code
interpreter = SimpleInterpreter(instructions)
interpreter.execute()

# Print the final symbol table (variable values)
print("Final Symbol Table:", interpreter.get_symbol_table())
```

### Full Example Workflow

Here’s how the full pipeline works:

1. **Input**: High-level code (like C or pseudo-code).
2. **Lexer**: Tokenize the source code into a list of tokens.
3. **Parser**: Convert the tokens into an abstract syntax tree (AST).
4. **IR Generation**: Generate intermediate representation (IR) instructions from the AST.
5. **Optimization**: Optimize the IR instructions (constant folding, dead code elimination).
6. **Target Code Generation**: Translate the optimized IR into target assembly-like code.
7. **Execution**: Execute the target code with an interpreter.

```python
from lexer import Lexer
from parser import Parser
from ir_generator import IRGenerator
from optimizer import IROptimizer
from code_gen import CodeGenerator
from interpreter import SimpleInterpreter

# Example high-level code
data = '''
int a = 5;
int b = 10;
int c = a + b;
print(c);
c = c - 5;
print(c);
'''

# 1. Tokenize the source code
lexer = Lexer()
tokens = lexer.tokenize(data)

# 2. Parse the tokens into an AST
parser = Parser()
ast = parser.parse(tokens)

# 3. Generate IR from the AST
ir_generator = IRGenerator()
instructions = ir_generator.generate(ast)

# 4. Optimize the IR instructions
optimizer = IROptimizer()
optimized_instructions = optimizer.optimize(instructions)

# 5. Generate target code
generator = CodeGenerator()
generator.generate_target_code(optimized_instructions)

# 6. Execute the target code
interpreter = SimpleInterpreter(generator.get_generated_code().split("
"))
interpreter.execute()

# 7. Print the final symbol table
print("Final Symbol Table:", interpreter.get_symbol_table())
```

### Output Example

```text
Original Instructions:
MOV a, 5
MOV b, 10
ADD c, a, b
PRINT c
SUB c, c, 5
PRINT c

Executing Instructions:
--------------------
15
10

Final Symbol Table: {'a': 5, 'b': 10, 'c': 10}
```

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests with improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Future Improvements

- **Advanced Optimizations**: Implement more sophisticated IR optimizations like loop unrolling or inlining functions.
- **Error Handling**: Add better error handling and debugging output for the interpreter.
- **Parser Extension**: Extend the parser to support a wider range of high-level language features, such as functions, arrays, etc.
- **Code Generation**: Generate code for specific target architectures, adding support for more complex operations and optimizations.
