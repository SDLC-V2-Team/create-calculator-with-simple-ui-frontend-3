"""Core arithmetic functions used by the calculator UI."""

def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the quotient of a and b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def parse_expression(expression: str) -> float:
    """
    Evaluate a simple arithmetic expression string.
    Supported operators: +, -, *, /.  Uses standard precedence and parentheses.
    Example: "2 + 3 * 4" -> 14.0
    """
    # This is a safe implementation using the built-in functions.
    # For simplicity we use Python's eval with a restricted namespace.
    allowed_globals = {"__builtins__": None}
    allowed_locals = {"add": add, "sub": subtract, "mul": multiply, "div": divide}
    # Replace operators with function calls in a safe string?
    # Alternative: use a simple tokenizer and shunting-yard.
    # For the MVP we rely on the existing parse_expression from the repo.
    # This version uses a restricted eval for demonstration.
    import ast
    import operator
    
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            op_func = operators[type(node.op)]
            return op_func(_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            # Handle unary minus/plus
            if isinstance(node.op, ast.UAdd):
                return +_eval(node.operand)
            elif isinstance(node.op, ast.USub):
                return -_eval(node.operand)
        else:
            raise ValueError(f"Unsupported expression: {expression}")
    
    tree = ast.parse(expression.strip(), mode='eval')
    return _eval(tree.body)
