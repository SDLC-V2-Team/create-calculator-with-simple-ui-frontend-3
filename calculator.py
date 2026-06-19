#!/usr/bin/env python3
"""Simple calculator CLI."""

import sys
import operator


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b


# Supported operators mapped to functions
OPERATORS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}


def parse_expression(expr):
    """Parse a simple 'operand operator operand' expression."""
    parts = expr.strip().split()
    if len(parts) != 3:
        raise ValueError("Expression must be in the form: operand operator operand (e.g., '2 + 3')")
    try:
        a = float(parts[0])
        b = float(parts[2])
    except ValueError:
        raise ValueError("Operands must be numeric.")
    op = parts[1]
    if op not in OPERATORS:
        raise ValueError(f"Unsupported operator '{op}'. Supported: {', '.join(OPERATORS.keys())}")
    return a, b, op


def calculate(a, b, op):
    """Perform arithmetic operation."""
    func = OPERATORS[op]
    return func(a, b)


def main():
    """Main CLI loop."""
    print("Simple Calculator CLI")
    print("Enter an expression in the form: operand operator operand")
    print("Supported operators: +, -, *, /")
    print("Type 'exit' or 'quit' to quit.")
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("Goodbye!")
                sys.exit(0)
            if not user_input:
                continue
            a, b, op = parse_expression(user_input)
            result = calculate(a, b, op)
            # Display result - if result is integer-like, show as int
            if result == int(result):
                print(int(result))
            else:
                print(result)
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
