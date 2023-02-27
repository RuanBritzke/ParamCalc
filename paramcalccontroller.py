from paramcalcview import ParamCalcWindow


class ParamCalcController:
    def __init__(self, model) -> None:
        self.model = model
        self.view = ParamCalcWindow(controller=self, model=self.model)

    def get_screen(self):
        return self.view
