"""
Core Python Calculator Engine for Shrey's Calc.
Provides safe, robust arithmetic operations, comprehensive scientific functions,
angle modes (DEG/RAD), and safe AST expression evaluation.
"""

import ast
import math
import operator
import re
from typing import Union, List, Dict, Any


class Calculator:
    """Mathematical computation engine with history tracking and safe AST evaluation."""

    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.angle_mode: str = "DEG"  # "DEG" or "RAD"

    # --- Basic Operations ---

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide a by b. Raises ZeroDivisionError if b is 0."""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Raise base to exponent."""
        try:
            return math.pow(base, exponent)
        except OverflowError:
            raise OverflowError("Result is too large")
        except ValueError:
            raise ValueError("Invalid mathematical operation (e.g. negative base with fractional power)")

    def percentage(self, a: float, b: float = 100.0) -> float:
        """Calculate percentage (a / 100)."""
        return a / 100.0

    def modulo(self, a: float, b: float) -> float:
        """Modulo operation a % b."""
        if b == 0:
            raise ZeroDivisionError("Cannot calculate modulo with zero")
        return a % b

    def square_root(self, a: float) -> float:
        """Square root of a number. Raises ValueError if a is negative."""
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(a)

    def cube_root(self, a: float) -> float:
        """Cube root of a number."""
        if a < 0:
            return -math.pow(-a, 1.0 / 3.0)
        return math.pow(a, 1.0 / 3.0)

    def negate(self, a: float) -> float:
        """Negate a number."""
        return -a

    def reciprocal(self, a: float) -> float:
        """Reciprocal 1/a."""
        if a == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return 1.0 / a

    def abs_val(self, a: float) -> float:
        """Absolute value |a|."""
        return abs(a)

    def factorial(self, a: float) -> int:
        """Factorial a!."""
        if a < 0 or not float(a).is_integer():
            raise ValueError("Factorial is only defined for non-negative integers")
        int_a = int(a)
        if int_a > 170:
            raise OverflowError("Factorial overflow (max 170!)")
        return math.factorial(int_a)

    # --- Scientific / Trigonometric Functions ---

    def sin(self, a: float, mode: str = None) -> float:
        mode = mode or self.angle_mode
        rad = math.radians(a) if mode == "DEG" else a
        val = math.sin(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def cos(self, a: float, mode: str = None) -> float:
        mode = mode or self.angle_mode
        rad = math.radians(a) if mode == "DEG" else a
        val = math.cos(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def tan(self, a: float, mode: str = None) -> float:
        mode = mode or self.angle_mode
        rad = math.radians(a) if mode == "DEG" else a
        cos_val = math.cos(rad)
        if abs(cos_val) < 1e-15:
            raise ValueError("Tangent is undefined for this angle (cos ≈ 0)")
        val = math.tan(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def asin(self, a: float, mode: str = None) -> float:
        if a < -1.0 or a > 1.0:
            raise ValueError("asin domain is [-1, 1]")
        res = math.asin(a)
        mode = mode or self.angle_mode
        return math.degrees(res) if mode == "DEG" else res

    def acos(self, a: float, mode: str = None) -> float:
        if a < -1.0 or a > 1.0:
            raise ValueError("acos domain is [-1, 1]")
        res = math.acos(a)
        mode = mode or self.angle_mode
        return math.degrees(res) if mode == "DEG" else res

    def atan(self, a: float, mode: str = None) -> float:
        res = math.atan(a)
        mode = mode or self.angle_mode
        return math.degrees(res) if mode == "DEG" else res

    def ln(self, a: float) -> float:
        """Natural logarithm (base e)."""
        if a <= 0:
            raise ValueError("Logarithm domain must be greater than 0")
        return math.log(a)

    def log10(self, a: float) -> float:
        """Logarithm base 10."""
        if a <= 0:
            raise ValueError("Logarithm domain must be greater than 0")
        return math.log10(a)

    def exp(self, a: float) -> float:
        """Exponential e^a."""
        try:
            return math.exp(a)
        except OverflowError:
            raise OverflowError("Result is too large")

    # --- AST Expression Evaluator ---

    def _eval_ast(self, node: ast.AST, angle_mode: str) -> Union[int, float]:
        """Recursively evaluate an AST node safely."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        if isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e
            raise ValueError(f"Undefined variable or constant '{node.id}'")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self._OPERATORS:
                operand = self._eval_ast(node.operand, angle_mode)
                return self._OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self._OPERATORS:
                left = self._eval_ast(node.left, angle_mode)
                right = self._eval_ast(node.right, angle_mode)

                if op_type is ast.Div:
                    if right == 0:
                        raise ZeroDivisionError("Cannot divide by zero")
                    return left / right

                if op_type is ast.Mod:
                    if right == 0:
                        raise ZeroDivisionError("Cannot calculate modulo with zero")
                    return left % right

                if op_type is ast.Pow:
                    if abs(right) > 1000 or (abs(left) > 10 and right > 200):
                        raise OverflowError("Exponentiation exceeds maximum allowed limits")
                    return self.power(left, right)

                return self._OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type}")

        if isinstance(node, ast.Call):
            func_name = getattr(node.func, "id", None)
            args = [self._eval_ast(arg, angle_mode) for arg in node.args]

            if func_name == "sqrt":
                if len(args) != 1: raise ValueError("sqrt() expects 1 argument")
                return self.square_root(args[0])
            if func_name == "cbrt":
                if len(args) != 1: raise ValueError("cbrt() expects 1 argument")
                return self.cube_root(args[0])
            if func_name == "sin":
                if len(args) != 1: raise ValueError("sin() expects 1 argument")
                return self.sin(args[0], angle_mode)
            if func_name == "cos":
                if len(args) != 1: raise ValueError("cos() expects 1 argument")
                return self.cos(args[0], angle_mode)
            if func_name == "tan":
                if len(args) != 1: raise ValueError("tan() expects 1 argument")
                return self.tan(args[0], angle_mode)
            if func_name == "asin":
                if len(args) != 1: raise ValueError("asin() expects 1 argument")
                return self.asin(args[0], angle_mode)
            if func_name == "acos":
                if len(args) != 1: raise ValueError("acos() expects 1 argument")
                return self.acos(args[0], angle_mode)
            if func_name == "atan":
                if len(args) != 1: raise ValueError("atan() expects 1 argument")
                return self.atan(args[0], angle_mode)
            if func_name == "ln":
                if len(args) != 1: raise ValueError("ln() expects 1 argument")
                return self.ln(args[0])
            if func_name in ("log", "log10"):
                if len(args) != 1: raise ValueError("log() expects 1 argument")
                return self.log10(args[0])
            if func_name == "exp":
                if len(args) != 1: raise ValueError("exp() expects 1 argument")
                return self.exp(args[0])
            if func_name == "abs":
                if len(args) != 1: raise ValueError("abs() expects 1 argument")
                return self.abs_val(args[0])
            if func_name in ("fact", "factorial"):
                if len(args) != 1: raise ValueError("factorial() expects 1 argument")
                return self.factorial(args[0])

            raise ValueError(f"Function call '{func_name}' is not permitted")

        raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")

    def evaluate_expression(self, expression: str, angle_mode: str = None) -> Union[int, float]:
        """
        Safely parse and evaluate a mathematical expression string.
        Transforms common scientific symbols (×, ÷, ^, √, π) into valid AST tokens.
        """
        if not expression or not expression.strip():
            raise ValueError("Expression is empty")

        mode = angle_mode or self.angle_mode
        clean_expr = expression.strip()

        # Symbol normalization
        clean_expr = clean_expr.replace("×", "*").replace("✕", "*")
        clean_expr = clean_expr.replace("÷", "/")
        clean_expr = clean_expr.replace("^", "**")
        clean_expr = clean_expr.replace("√", "sqrt")
        clean_expr = clean_expr.replace("π", "pi")
        clean_expr = clean_expr.replace("mod", "%")

        # Factorial notation: 5! -> fact(5)
        clean_expr = re.sub(r'(\d+)!', r'fact(\1)', clean_expr)

        # Implicit multiplication: 2pi -> 2 * pi, 2(3) -> 2 * (3)
        clean_expr = re.sub(r'(\d)\s*(pi|e|\()', r'\1 * \2', clean_expr)
        clean_expr = re.sub(r'(\))\s*(\d|pi|e|\()', r'\1 * \2', clean_expr)

        # Trim trailing operator if user submitted incomplete expression like "8 +"
        clean_expr = re.sub(r'[\+\-\*\/\%]\s*$', '', clean_expr).strip()

        try:
            tree = ast.parse(clean_expr, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid mathematical syntax: {str(e)}")

        raw_result = self._eval_ast(tree.body, mode)

        if isinstance(raw_result, (float, int)):
            if math.isnan(raw_result) or math.isinf(raw_result):
                raise OverflowError("Result is undefined or infinite")

        if isinstance(raw_result, float) and raw_result.is_integer() and abs(raw_result) < 1e15:
            result = int(raw_result)
        else:
            result = round(raw_result, 10) if isinstance(raw_result, float) else raw_result
            if isinstance(result, float) and result.is_integer():
                result = int(result)

        self.add_history(expression, result)
        return result

    def add_history(self, expression: str, result: Union[int, float]):
        """Record calculation in history."""
        self.history.append({
            "expression": expression,
            "result": result,
            "formatted": str(result)
        })
        if len(self.history) > 50:
            self.history.pop(0)

    def get_history(self) -> List[Dict[str, Any]]:
        """Return history in reverse chronological order."""
        return list(reversed(self.history))

    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()
