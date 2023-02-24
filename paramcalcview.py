from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class WarningPopup(Popup):
    def __init__(self, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ParamCalcWindow(Screen):

    toggles_previous_state = "normaldown"

    def __init__(self, **kw):
        super(ParamCalcWindow, self).__init__(**kw)

    def clear_entry(self, instance: TextInput):
        instance.text = ""
        pass

    def clear_all(self):
        self.ids.PotenciaAparente.text = ""
        self.ids.PotenciaAtiva.text = ""
        self.ids.PotenciaReativa.text = ""
        self.ids.cosphi.text = ""
        self.ids.phi.text = ""
        self.ids.Reatancia.text = ""
        self.ids.Tensao.text = ""
        self.ids.Corrente.text = ""
        pass

    def get_entries(self):
        return [
            float(self.ids.PotenciaAparente.text)
            if self.ids.PotenciaAparente.text
            else None,
            float(self.ids.PotenciaAtiva.text) if self.ids.PotenciaAtiva.text else None,
            float(self.ids.PotenciaReativa.text)
            if self.ids.PotenciaReativa.text
            else None,
            self.filter_TextInput(self.ids.cosphi, lower_limit=0, upper_limit=1),
            self.filter_TextInput(self.ids.phi, lower_limit=-90, upper_limit=90),
            self.ids.Reatancia.text if self.ids.Reatancia.text else None,
            float(self.ids.Tensao.text) if self.ids.Tensao.text else None,
            float(self.ids.Corrente.text) if self.ids.Corrente.text else None,
        ]

    def filter_TextInput(
        self, instance: TextInput, lower_limit: float, upper_limit: float
    ) -> float | None:
        text = instance.text

        if not text:
            return None
        value = float(text)
        if lower_limit <= value <= upper_limit:
            return instance
        warning = WarningPopup()
        warning.message.text = instance.hint_text + " fora do intervalo permitido"
        self.clear_entry(instance)
        warning.open()

    def get_mode(self):
        return [self.ids.trifasico.state, self.ids.monofasico.state]

    def check_toggles(self):

        if self.ids.trifasico.state == self.ids.monofasico.state:
            if self.toggles_previous_state == "normaldown":
                self.ids.trifasico.state = "down"
                self.ids.monofasico.satte = "normal"
            else:
                self.ids.trifasico.state = "normal"
                self.ids.monofasico.state = "down"

        self.toggles_previous_state = (
            self.ids.trifasico.state + self.ids.monofasico.state
        )
