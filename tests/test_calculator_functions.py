"""Tests for calculator_functions.py — arithmetic functions and expression parser."""

import pytest
from calculator_functions import add, subtract, multiply, divide, parse_expression


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_add_two_positive_integers(self):
        assert add(2, 3) == 5

    def test_add_positive_and_negative(self):
        assert add(10, -4) == 6

    def test_add_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_zeroes(self):
        assert add(0, 0) == 0


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(10, 3) == 7

    def test_subtract_yields_negative(self):
        assert subtract(3, 10) == -7

    def test_subtract_floats(self):
        assert subtract(5.5, 2.2) == pytest.approx(3.3)


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_multiply_two_positives(self):
        assert multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0

    def test_multiply_negative_numbers(self):
        assert multiply(-3, -4) == 12

    def test_multiply_float(self):
        assert multiply(2.5, 4) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_divide_exact(self):
        assert divide(10, 2) == 5.0

    def test_divide_float_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_negative_numerator(self):
        assert divide(-9, 3) == pytest.approx(-3.0)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_zero_numerator(self):
        assert divide(0, 5) == 0.0


# ---------------------------------------------------------------------------
# parse_expression
# ---------------------------------------------------------------------------

class TestParseExpression:
    def test_simple_addition(self):
        assert parse_expression("2 + 3") == pytest.approx(5.0)

    def test_operator_precedence(self):
        # 2 + 3 * 4 should evaluate to 14, not 20
        assert parse_expression("2 + 3 * 4") == pytest.approx(14.0)

    def test_parentheses_override_precedence(self):
        assert parse_expression("(2 + 3) * 4") == pytest.approx(20.0)

    def test_division_in_expression(self):
        assert parse_expression("10 / 4") == pytest.approx(2.5)

    def test_unary_minus(self):
        assert parse_expression("-5 + 3") == pytest.approx(-2.0)

    def test_unary_plus(self):
        assert parse_expression("+7 - 2") == pytest.approx(5.0)

    def test_nested_parentheses(self):
        assert parse_expression("((2 + 3) * (1 + 1))") == pytest.approx(10.0)

    def test_whitespace_handling(self):
        assert parse_expression("  4 + 6  ") == pytest.approx(10.0)

    def test_invalid_expression_raises(self):
        with pytest.raises((ValueError, SyntaxError, TypeError, ZeroDivisionError)):
            parse_expression("2 + ")

    def test_unsupported_expression_raises(self):
        # A call expression is not in our supported AST nodes
        with pytest.raises((ValueError, TypeError, AttributeError)):
            parse_expression("abs(-1)")