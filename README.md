# Calculator Application

A simple yet functional calculator with a graphical user interface built using Tkinter.

## Features
- Basic arithmetic: addition, subtraction, multiplication, division
- Expression parsing with parentheses support
- Clear and backspace buttons
- Decimal point support
- Error handling (division by zero, invalid expressions)

## Architecture

The application follows a clean separation of concerns:

- `calculator_functions.py`: Contains the core arithmetic logic (`add`, `subtract`, `multiply`, `divide`) and a safe expression parser (`parse_expression`).
- `ui.py`: Implements the Tkinter GUI that interacts with the core functions.
- `main.py`: Entry point to launch the application.

## Getting Started

### Prerequisites
- Python 3.7 or later (Tkinter is included in the standard library)
- (Optional) `pytest` for running tests

### Running the Calculator

```bash
python main.py
```

### Running Tests

```bash
pip install -r requirements.txt
pytest tests/
```

## Design Decisions

This project was created to align the UI with the pre-existing calculator functions, as outlined in ADR-001. The UI directly calls the core functions for all operations, ensuring consistency and maintainability.

## License

This project is provided as a scaffold for demonstration purposes.
