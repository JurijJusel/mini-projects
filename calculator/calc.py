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

    def update_display(self):
        # Show history + current input
        self.ids.display.text = self.history_text + self.current_expression

class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == "__main__":
    CalculatorApp().run()
