from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


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
        try:
            result = str(eval(self.current_expression))
            # Append expression + result to history
            self.history_text += f"{self.current_expression} = {result}\n"
            # Reset current expression
            self.current_expression = ""
            self.update_display()
        except Exception:
            self.history_text += f"{self.current_expression} = Error\n"
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
