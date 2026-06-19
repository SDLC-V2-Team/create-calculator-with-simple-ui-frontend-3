import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import (
    add,
    subtract,
    multiply,
    divide,
    OPERATORS,
    parse_expression,
    calculate,
)


# --- Tests for add ---
def test_add_happy_path():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -4) == -5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


# --- Tests for subtract ---
def test_subtract_happy_path():
    assert subtract(10, 4) == 6


def test_subtract_results_in_negative():
    assert subtract(3, 7) == -4


# --- Tests for multiply ---
def test_multiply_happy_path():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(100, 0) == 0


# --- Tests for divide ---
def test_divide_happy_path():
    assert divide(10, 2) == 5.0


def test_divide_float_result():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        divide(5, 0)


# --- Tests for OPERATORS dict ---
def test_operators_dict_contains_all_expected_keys():
    assert set(OPERATORS.keys()) == {'+', '-', '*', '/'}


def test_operators_dict_maps_to_correct_functions():
    assert OPERATORS['+'] is add
    assert OPERATORS['-'] is subtract
    assert OPERATORS['*'] is multiply
    assert OPERATORS['/'] is divide


# --- Tests for parse_expression ---
def test_parse_expression_valid_addition():
    a, b, op = parse_expression("2 + 3")
    assert a == 2.0
    assert b == 3.0
    assert op == '+'


def test_parse_expression_valid_subtraction():
    a, b, op = parse_expression("10 - 4")
    assert a == 10.0
    assert b == 4.0
    assert op == '-'


def test_parse_expression_valid_floats():
    a, b, op = parse_expression("1.5 * 2.0")
    assert a == 1.5
    assert b == 2.0
    assert op == '*'


def test_parse_expression_invalid_operator():
    with pytest.raises(ValueError, match="Unsupported operator"):
        parse_expression("2 ^ 3")


def test_parse_expression_invalid_operand_not_numeric():
    with pytest.raises(ValueError, match="Operands must be numeric."):
        parse_expression("a + 3")


def test_parse_expression_wrong_format_too_few_parts():
    with pytest.raises(ValueError, match="Expression must be in the form"):
        parse_expression("2 +")


def test_parse_expression_wrong_format_too_many_parts():
    with pytest.raises(ValueError, match="Expression must be in the form"):
        parse_expression("2 + 3 + 4")


def test_parse_expression_empty_string():
    with pytest.raises(ValueError, match="Expression must be in the form"):
        parse_expression("")


# --- Tests for calculate ---
def test_calculate_addition():
    assert calculate(3, 4, '+') == 7


def test_calculate_subtraction():
    assert calculate(9, 3, '-') == 6


def test_calculate_multiplication():
    assert calculate(6, 7, '*') == 42


def test_calculate_division():
    assert calculate(15, 3, '/') == 5.0


def test_calculate_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        calculate(5, 0, '/')