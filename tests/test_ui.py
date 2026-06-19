"""Tests for CalculatorUI in ui.py."""

import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock

from ui import CalculatorUI


@pytest.fixture
def app(request):
    """Create a CalculatorUI instance with a real Tk root."""
    root = tk.Tk()
    root.withdraw()  # Hide the window during tests
    calculator = CalculatorUI(root)
    yield calculator
    root.destroy()


class TestCalculatorUIInit:
    def test_initial_display_is_zero(self, app):
        """Happy path: display should show '0' on startup."""
        assert app.display_var.get() == "0"

    def test_initial_expression_is_empty(self, app):
        """Happy path: internal expression should be empty string on startup."""
        assert app.expression == ""

    def test_buttons_created(self, app):
        """Happy path: key buttons should exist in the buttons dict."""
        expected_buttons = {'7', '8', '9', '/', '4', '5', '6', '*',
                            '1', '2', '3', '-', 'C', '0', '.', '+', '=', '←'}
        assert expected_buttons == set(app.buttons.keys())


class TestOnButtonClick:
    def test_digit_appended_to_expression(self, app):
        """Happy path: clicking a digit appends it to expression and updates display."""
        app._on_button_click('5')
        assert app.expression == "5"
        assert app.display_var.get() == "5"

    def test_multiple_digits_and_operator(self, app):
        """Happy path: clicking digits and operator builds the expression correctly."""
        for char in ['1', '2', '+', '3']:
            app._on_button_click(char)
        assert app.expression == "12+3"
        assert app.display_var.get() == "12+3"

    def test_evaluate_simple_addition(self, app):
        """Happy path: '=' evaluates the expression using parse_expression."""
        with patch('ui.parse_expression', return_value=15) as mock_parse:
            app.expression = "10+5"
            app._on_button_click('=')
            mock_parse.assert_called_once_with("10+5")
            assert app.display_var.get() == "15"
            assert app.expression == "15"

    def test_clear_resets_state(self, app):
        """Happy path: 'C' clears the expression and resets display to '0'."""
        app.expression = "123"
        app.display_var.set("123")
        app._on_button_click('C')
        assert app.expression == ""
        assert app.display_var.get() == "0"

    def test_backspace_removes_last_char(self, app):
        """Edge case: '←' removes the last character from the expression."""
        app.expression = "123"
        app.display_var.set("123")
        app._on_button_click('←')
        assert app.expression == "12"
        assert app.display_var.get() == "12"

    def test_backspace_on_single_char_resets_to_zero(self, app):
        """Edge case: '←' on a single-character expression resets display to '0'."""
        app.expression = "5"
        app.display_var.set("5")
        app._on_button_click('←')
        assert app.expression == "0"
        assert app.display_var.get() == "0"

    def test_evaluate_division_by_zero_shows_error(self, app):
        """Error path: ZeroDivisionError during evaluation shows 'Error' and clears expression."""
        with patch('ui.parse_expression', side_effect=ZeroDivisionError("division by zero")):
            app.expression = "5/0"
            app._on_button_click('=')
            assert app.display_var.get() == "Error"
            assert app.expression == ""

    def test_evaluate_invalid_expression_shows_error(self, app):
        """Error path: ValueError during evaluation shows 'Error' and clears expression."""
        with patch('ui.parse_expression', side_effect=ValueError("invalid expression")):
            app.expression = "1++2"
            app._on_button_click('=')
            assert app.display_var.get() == "Error"
            assert app.expression == ""

    def test_evaluate_syntax_error_shows_error(self, app):
        """Error path: SyntaxError during evaluation shows 'Error' and clears expression."""
        with patch('ui.parse_expression', side_effect=SyntaxError("bad syntax")):
            app.expression = "1+"
            app._on_button_click('=')
            assert app.display_var.get() == "Error"
            assert app.expression == ""