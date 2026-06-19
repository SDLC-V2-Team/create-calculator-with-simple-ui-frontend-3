"""Tkinter-based calculator UI that calls the core calculator functions."""

import tkinter as tk
from calculator_functions import parse_expression, add, subtract, multiply, divide

class CalculatorUI:
    """Main calculator window."""

    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self._create_widgets()

    def _create_widgets(self):
        # Display
        display_frame = tk.Frame(self.root, height=60)
        display_frame.pack(expand=True, fill='both', padx=5, pady=5)

        entry = tk.Entry(display_frame, textvariable=self.display_var, font=('Arial', 20),
                         justify='right', state='readonly', relief='sunken', bd=10)
        entry.pack(expand=True, fill='both')

        # Buttons layout
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True, fill='both', padx=5, pady=(0, 5))

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '.', '+'],
            ['=', '←']
        ]

        for row_idx, row in enumerate(buttons):
            row_frame = tk.Frame(button_frame)
            row_frame.pack(expand=True, fill='both')
            for col_idx, text in enumerate(row):
                btn = tk.Button(row_frame, text=text, font=('Arial', 14),
                                command=lambda t=text: self._on_button_click(t))
                # Make '=' span two columns in the last row
                if text == '=':
                    btn.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)
                    continue
                btn.grid(row=0, column=col_idx, sticky='nsew', padx=2, pady=2)
                row_frame.grid_columnconfigure(col_idx, weight=1)
            row_frame.grid_columnconfigure(len(row), weight=1)  # extra column for '=' in last row
        # Force grid for '=' in last row: we placed it manually above, need to adjust.
        # Actually a cleaner approach: define rows and columns explicitly.
        self._create_button_grid(button_frame)

    def _create_button_grid(self, parent):
        """Create a proper grid of buttons."""
        # Clear any previous widgets (just in case)
        for widget in parent.winfo_children():
            widget.destroy()

        self.buttons = {}
        button_data = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('C', 3, 0), ('0', 3, 1), ('.', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 2), ('←', 4, 2)  # '=' spans two columns, backspace at column 2, spans 2 as well? Let's do two separate
        ]
        # Redo: last row: '=' spans columns 0-1, '←' spans columns 2-3
        btn_data = [
            ('7', 0, 0, 1, 1), ('8', 0, 1, 1, 1), ('9', 0, 2, 1, 1), ('/', 0, 3, 1, 1),
            ('4', 1, 0, 1, 1), ('5', 1, 1, 1, 1), ('6', 1, 2, 1, 1), ('*', 1, 3, 1, 1),
            ('1', 2, 0, 1, 1), ('2', 2, 1, 1, 1), ('3', 2, 2, 1, 1), ('-', 2, 3, 1, 1),
            ('C', 3, 0, 1, 1), ('0', 3, 1, 1, 1), ('.', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('=', 4, 0, 1, 2), ('←', 4, 2, 1, 2)
        ]

        for text, row, col, rowspan, colspan in btn_data:
            btn = tk.Button(parent, text=text, font=('Arial', 14),
                            command=lambda t=text: self._on_button_click(t))
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                     sticky='nsew', padx=2, pady=2)
            self.buttons[text] = btn

        # Configure grid weights
        for i in range(5):
            parent.grid_rowconfigure(i, weight=1)
        for j in range(4):
            parent.grid_columnconfigure(j, weight=1)

    def _on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif char == '←':
            self.expression = self.expression[:-1]
            if not self.expression:
                self.expression = "0"
            self.display_var.set(self.expression)
        elif char == '=':
            try:
                result = parse_expression(self.expression)
                self.display_var.set(str(result))
                self.expression = str(result)
            except (ZeroDivisionError, ValueError, SyntaxError) as e:
                self.display_var.set("Error")
                self.expression = ""
        else:
            # Append digit or operator
            self.expression += str(char)
            self.display_var.set(self.expression)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorUI(root)
    app.run()
