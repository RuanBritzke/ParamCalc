from paramcalcview import ParamCalcView, WarningPopup, TextInput, ToggleButton, Widget


class ParamCalcController:
    def __init__(self, model) -> None:
        self.model = model
        self.view = ParamCalcView(controller=self, model=self.model)

    def get_screen(self) -> None:
        """
        Cria a janela
        """
        return self.view

    def set_attribute(self, kw, value):
        setattr(self.model, kw, value)
        self.model.evaluate()

    def set_mode(self, value):
        self.model._mode = value

    def filter_TextInput(
        self,
        instance,
        kw=None,
        value=None,
        *,
        lower_limit: float = None,
        upper_limit: float = None,
    ) -> float | None:
        if value is None:
            self.set_attribute(kw, value)
            return
        if isinstance(lower_limit, (int, float)) and isinstance(
            upper_limit, (int, float)
        ):
            if lower_limit <= value <= upper_limit:
                self.set_attribute(kw, value)
                return
        if upper_limit is None:
            if lower_limit <= value:
                self.set_attribute(kw, value)
                return

        warning = WarningPopup()
        warning.title = "Aviso"
        warning.message.text = (
            instance.hint_text + f" fora do intervalo [{lower_limit}, {upper_limit}]"
        )
        self.text_input_clear(instance)
        warning.open()
        return ""

    def text_input_clear(self, *instances):
        """
        Limpa os campos de texto.
        """
        for instance in instances:
            instance.text = ""

    def clear_all(self):
        for instance in self.view.walk():
            if isinstance(instance, TextInput):
                instance.text = ""
            if isinstance(instance, ToggleButton):
                if instance.name == "trifasico":
                    if instance.state == "down":
                        instance.state = "normal"
                        self.view.ids.monofasico.state = "down"
        self.model.reset()
