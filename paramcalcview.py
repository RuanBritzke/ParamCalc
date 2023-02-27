from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
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
    Window.size = (int(900 / 3), int(1600 / 3))
    Window.minimum_width, Window.minimum_height = Window.size


    controller = ObjectProperty()
    model = ObjectProperty()
    toggles_previous_state = "normaldown"


    def __init__(self, **kw):
        super(ParamCalcWindow, self).__init__(**kw)
        self._createInputs()

    def _createInputs(self):
        # iteractivaly creates all text inputs.
        pass

    def Enabler(self, *instances):
        instance: Widget
        for instance in instances:
            instance.disabled = False

    def Disabler(self, *instances):
        instance: Widget
        for instance in instances:
            instance.disabled = True

    def clear_entry(self, *instances):
        instance: Widget
        for instance in instances:
            instance.text = ""

    def clear_all(self):
        self.clear_entry(
            self.ids.PotenciaAparente,
            self.ids.PotenciaAtiva,
            self.ids.PotenciaReativa,
            self.ids.CosPhi,
            self.ids.Phi,
            self.ids.Tensao,
            self.ids.Corrente,
        )
        self.ids.Reatancia.text = "Capacitivo Indutivo"
        self.Enabler(
            self.ids.PotenciaAparente,
            self.ids.PotenciaAtiva,
            self.ids.PotenciaReativa,
            self.ids.CosPhi,
            self.ids.Phi,
            self.ids.Reatancia,
            self.ids.Tensao,
            self.ids.Corrente,
        )

    def get_entries(self):
        return [
            self.get_mode(),
            float(self.ids.PotenciaAparente.text)
            if self.ids.PotenciaAparente.text
            else None,
            float(self.ids.PotenciaAtiva.text) if self.ids.PotenciaAtiva.text else None,
            float(self.ids.PotenciaReativa.text)
            if self.ids.PotenciaReativa.text
            else None,
            self.filter_TextInput(self.ids.CosPhi, lower_limit=0, upper_limit=1),
            self.filter_TextInput(self.ids.Phi, lower_limit=-90, upper_limit=90),
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
        warning.title = "Aviso"
        warning.message.text = instance.hint_text + " fora do intervalo permitido"
        self.clear_entry(instance)
        warning.open()

    def get_mode(self):
        return (self.ids.trifasico.state, self.ids.monofasico.state)

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

    def TextInputDisabler(self, instance) -> None:
        """
        Prototype for future use
        """

        # if not instance.text:
        #     return
        # match instance.name:
        #     case "PotenciaAparente":
        #         if self.ids.PotenciaAtiva.text:
        #             self.Disabler(self.ids.PotenciaReativa, self.ids.CosPhi)
        #         if self.ids.PotenciaReativa.text:
        #             self.Disabler(
        #                 self.ids.PotenciaAtiva,
        #                 self.ids.CosPhi,
        #                 self.ids.Phi,
        #                 self.ids.Reatancia,
        #             )
        #         if self.ids.CosPhi.text or self.ids.Phi.text:
        #             self.Disabler(self.ids.PotenciaAtiva, self.ids.PotenciaReativa)
        #         if self.ids.Tensao.text:
        #             self.Disabler(self.ids.Corrente)
        #         if self.ids.Corrente.text:
        #             self.Disabler(self.ids.Tensao)
        #     case "PotenciaAtiva":
        #         if self.ids.PotenciaAparente.text:
        #             self.Disabler(
        #                 self.ids.PotenciaReativa, self.ids.CosPhi, self.ids.Phi
        #             )
        #         if self.ids.PotenciaReativa.text:
        #             self.Disabler(
        #                 self.ids.PotenciaAparente,
        #                 self.ids.CosPhi,
        #                 self.ids.Phi,
        #                 self.ids.Reatancia,
        #             )
        #         if self.ids.CosPhi.text:
        #             self.Disabler(self.ids.PotenciaAparente, self.ids.Phi)
        #         if self.ids.Phi.text:
        #             self.Disabler(self.ids.PotenciaAparente, self.ids.PotenciaReativa)
        #         if self.ids.Tensao.text and (
        #             self.ids.CosPhi.text or self.ids.Phi.text
        #         ):
        #             self.Disabler(self.ids.Corrente)

        #     case "Phi":
        #         self.Disabler(self.ids.CosPhi, self.ids.Reatancia)
        return


class ParamCalcApp(App):
    def build(self):
        return ParamCalcWindow()


if __name__ == "__main__":
    ParamCalcApp().run()
