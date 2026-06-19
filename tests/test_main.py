"""Tests for main.py entry point."""

import sys
import types
from unittest.mock import MagicMock, patch, call
import pytest


@pytest.fixture
def mock_tk(monkeypatch):
    """Fixture that mocks tkinter.Tk."""
    mock_root = MagicMock()
    mock_tk_class = MagicMock(return_value=mock_root)
    monkeypatch.setattr("tkinter.Tk", mock_tk_class)
    return mock_tk_class, mock_root


@pytest.fixture
def mock_calculator_ui(monkeypatch):
    """Fixture that mocks CalculatorUI."""
    mock_app = MagicMock()
    mock_ui_class = MagicMock(return_value=mock_app)
    monkeypatch.setattr("ui.CalculatorUI", mock_ui_class)
    return mock_ui_class, mock_app


def test_main_creates_tk_root(mock_tk, mock_calculator_ui):
    """Happy path: main() creates a tkinter Tk root window."""
    mock_tk_class, mock_root = mock_tk

    with patch("tkinter.Tk", mock_tk_class):
        with patch("ui.CalculatorUI", mock_calculator_ui[0]):
            import importlib
            import main
            importlib.reload(main)
            main.main()

    mock_tk_class.assert_called_once()


def test_main_instantiates_calculator_ui(mock_tk, mock_calculator_ui):
    """Happy path: main() instantiates CalculatorUI with the root window."""
    mock_tk_class, mock_root = mock_tk
    mock_ui_class, mock_app = mock_calculator_ui

    with patch("tkinter.Tk", mock_tk_class):
        with patch("ui.CalculatorUI", mock_ui_class):
            import importlib
            import main
            importlib.reload(main)
            main.main()

    mock_ui_class.assert_called_once_with(mock_root)


def test_main_calls_app_run(mock_tk, mock_calculator_ui):
    """Happy path: main() calls run() on the CalculatorUI instance."""
    mock_tk_class, mock_root = mock_tk
    mock_ui_class, mock_app = mock_calculator_ui

    with patch("tkinter.Tk", mock_tk_class):
        with patch("ui.CalculatorUI", mock_ui_class):
            import importlib
            import main
            importlib.reload(main)
            main.main()

    mock_app.run.assert_called_once()


def test_main_called_multiple_times(mock_tk, mock_calculator_ui):
    """Edge case: main() can be called multiple times, each time creating new instances."""
    mock_tk_class, mock_root = mock_tk
    mock_ui_class, mock_app = mock_calculator_ui

    with patch("tkinter.Tk", mock_tk_class):
        with patch("ui.CalculatorUI", mock_ui_class):
            import importlib
            import main
            importlib.reload(main)
            main.main()
            main.main()

    assert mock_tk_class.call_count == 2
    assert mock_ui_class.call_count == 2
    assert mock_app.run.call_count == 2


def test_main_ui_import_error():
    """Error path: ImportError is raised if CalculatorUI cannot be imported."""
    # Temporarily remove the 'ui' module to simulate import failure
    original_ui = sys.modules.get("ui")
    sys.modules["ui"] = None  # Force ImportError on import

    try:
        import importlib
        # Re-import main with broken ui module
        with pytest.raises((ImportError, AttributeError)):
            import main
            importlib.reload(main)
            main.main()
    finally:
        # Restore original state
        if original_ui is not None:
            sys.modules["ui"] = original_ui
        elif "ui" in sys.modules:
            del sys.modules["ui"]