from kivy.app import App
from paramcalcmodel import ParamCalcModel
from paramcalcview import ParamCalcWindow


class ParamCalcController:
    def __init__(self, model) -> None:
        self.model = model
        self.view = ParamCalcWindow(controller=self, model=self.model)

    def get_screen(self):
        return self.view


class ParamCalcApp(App):
    def build(self):
        return ParamCalcWindow()


if __name__ == "__main__":
    ParamCalcApp().run()
00
