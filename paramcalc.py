from kivy.app import App
from paramcalcmodel import ParamCalcModel
from paramcalcview import ParamCalcWindow


class ParamCalcApp(App):
    def build(self):
        return ParamCalcWindow()


if __name__ == "__main__":
    ParamCalcApp().run()
