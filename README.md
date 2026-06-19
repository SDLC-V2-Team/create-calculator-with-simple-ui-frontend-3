# Simple Calculator CLI

A minimal calculator that supports basic arithmetic operations via a command-line interface.

## Usage

Run the script:

```bash
python calculator.py
```

Then enter expressions in the format `operand operator operand`, for example:

```
> 2 + 3
5
> 10.5 * 2
21.0
> 8 / 4
2
> 5 - 9
-4
```

Type `exit` or `quit` to stop.

## Supported Operators

- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)

## Testing

Tests use `pytest`. Install and run:

```bash
pip install pytest
pytest tests/
```

## Design Decision

Implemented as a single Python script with a CLI, following the architecture decision record (ADR-001 and ADR-002). No external dependencies or web framework required.
