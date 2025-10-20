from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import re

Window.size = (400, 600)
Window.clearcolor = (0.2, 0.3, 0.4, 1)  # RGBA background color


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_expression = ""
        self.history_text = ""

    def button_pressed(self, button):
        # Append number/operator to current expression
        self.current_expression += button.text
        self.update_display()

    def clear_display(self):
        # Clear everything
        self.current_expression = ""
        self.history_text = ""
        self.update_display()

    def calculate_result(self):
        expr = self.current_expression.strip()

        # Basic validation — expression must not be empty and must end with a number
        if not expr or not expr[-1].isdigit():
            return

        # Prevent double operators like ++, --, +*, etc.
        if re.search(r'[\+\-\*/]{2,}', expr):
            return

        try:
            # Safe evaluation — only numbers and operators allowed
            if re.match(r'^[\d\+\-\*/\. ]+$', expr):
                result = str(eval(expr))
                self.history_text += f"{expr} = {result}\n"
            else:
                return

        except Exception:
            # Any runtime error (e.g., division by zero)
            return

        # Clear expression and update display
        self.current_expression = ""
        self.update_display()

    def round_number(self):
        """Round the last number or result"""
        text = self.current_expression.strip()
        if not text:
            # Try to round the last result from history
            if self.history_text.strip():
                last_line = self.history_text.strip().split("\n")[-1]
                if "=" in last_line:
                    try:
                        result = float(last_line.split("=")[-1].strip())
                        rounded = round(result)
                        self.history_text += f"Round: {rounded}\n"
                        self.update_display()
                        return
                    except:
                        return
            return

        # Round the current number being entered
        try:
            value = float(text)
            rounded = round(value)
            self.current_expression = str(rounded)
            self.update_display()
        except ValueError:
            return

    def area(self):
        """Calculate area from two numbers (like width*height)"""
        text = self.current_expression.strip()

        # Extract numbers from the current expression
        numbers = re.findall(r"[-+]?\d*\.?\d+", text)

        if len(numbers) == 2:
            a = float(numbers[0])
            b = float(numbers[1])
            area = a * b
            self.history_text += f"Area ({a} x {b}) = {area}\n"
            self.current_expression = ""
            self.update_display()
        else:
            # Not enough numbers entered — show quick help
            self.history_text += "Enter 2 numbers (e.g. 5&10) then press 'area' button\n"
            self.update_display()

    def update_display(self):
        # Show history + current input
        self.ids.display.text = self.history_text + self.current_expression

class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == "__main__":
    CalculatorApp().run()
