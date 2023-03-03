import os
from kivy.app import App
from paramcalcmodel import ParamCalcModel
from paramcalccontroller import ParamCalcController


class ParamCalcApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = ParamCalcModel()
        self.controller = ParamCalcController(self.model)

    def build(self):
        return self.controller.get_screen()


if __name__ == "__main__":
    ParamCalcApp().run()
