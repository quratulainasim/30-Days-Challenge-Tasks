
import re

class CalculatorError(Exception):
    pass

def parse_expression(expression: str):
    # This is a basic tokenizer; a full parser would build an AST
    tokens = re.findall(r'\d+\.\d+|\d+|\+|\-|\*|\/|\(|\)', expression)
    return tokens

def validate_expression(tokens):
    # Check for balanced parentheses
    balance = 0
    for token in tokens:
        if token == '(':
            balance += 1
        elif token == ')':
            balance -= 1
        if balance < 0:
            raise CalculatorError("Mismatched parentheses")
    if balance != 0:
        raise CalculatorError("Mismatched parentheses")

    # Check for invalid characters (should be caught by tokenizer, but as a safeguard)
    for token in tokens:
        if not re.fullmatch(r'\d+\.\d+|\d+|\+|\-|\*|\/|\(|\)', token):
            raise CalculatorError(f"Invalid character in expression: {token}")

    # Check for consecutive operators or operators at start/end
    operators = {'+', '-', '*', '/'}
    if not tokens:
        raise CalculatorError("Empty expression")

    # Check for operators at the beginning or end of the expression
    if tokens[0] in operators or tokens[-1] in operators:
        raise CalculatorError("Expression cannot start or end with an operator")

    for i in range(len(tokens) - 1):
        if tokens[i] in operators and tokens[i+1] in operators:
            raise CalculatorError("Consecutive operators")
        if tokens[i] == '(' and tokens[i+1] in operators - {'-'}: # Allow unary minus
            raise CalculatorError("Operator immediately after opening parenthesis")
        if tokens[i] in operators and tokens[i+1] == ')':
            raise CalculatorError("Operator immediately before closing parenthesis")
        if tokens[i] == ')' and tokens[i+1] == '(':
            raise CalculatorError("Missing operator between parentheses")
        if re.fullmatch(r'\d+\.\d+|\d+', tokens[i]) and tokens[i+1] == '(':
             raise CalculatorError("Missing operator between number and parenthesis")
        if tokens[i] == ')' and re.fullmatch(r'\d+\.\d+|\d+', tokens[i+1]):
             raise CalculatorError("Missing operator between parenthesis and number")

    return True

def evaluate_expression(tokens):
    # This is a very basic evaluation for demonstration, not a full shunting-yard or AST evaluator
    # For a real calculator, use a proper expression parser/evaluator library or implement a shunting-yard algorithm.
    try:
        # Join tokens into a string for eval, ensuring spaces are handled if any
        expression_str = " ".join(tokens)

        # Security check: restrict allowed names in eval to prevent arbitrary code execution
        # Use a restricted set of global and local variables.
        # This is still a high-risk operation and should be avoided in production.
        allowed_builtins = {'abs', 'max', 'min', 'round', 'pow', 'sum'}
        safe_dict = {
            key: value for key, value in __builtins__.__dict__.items() if key in allowed_builtins
        }

        # Perform calculation
        result = eval(expression_str, {"__builtins__": safe_dict})
        return float(result)
    except ZeroDivisionError:
        raise CalculatorError("Division by zero is not allowed.")
    except Exception as e:
        raise CalculatorError(f"Error evaluating expression: {e}")

import sys

def calculate(expression: str):
    """
    Main function to parse, validate, and evaluate a mathematical expression.
    """
    # Remove all whitespace from the expression for easier parsing
    expression = expression.replace(" ", "")

    tokens = parse_expression(expression)
    validate_expression(tokens)
    return evaluate_expression(tokens)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        try:
            result = calculate(expression)
            print(f"Result: {result}")
        except CalculatorError as e:
            print(f"Error: {e}")
    else:
        print("Interactive Calculator. Type 'exit' to quit.")
        while True:
            expression = input("Enter expression: ")
            if expression.lower() == 'exit':
                break
            if not expression.strip():
                continue
            try:
                result = calculate(expression)
                print(f"Result: {result}")
            except CalculatorError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
