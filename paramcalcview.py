import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
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


class ParamCalcView(Screen):
    Window.size = (int(900 / 3), int(1600 / 3))
    Window.minimum_width, Window.minimum_height = Window.size

    controller = ObjectProperty()
    model = ObjectProperty()
    toggles_previous_state = "normaldown"

    def __init__(self, **kw):
        super(ParamCalcView, self).__init__(**kw)
        self.model.add_observer(self)

    def check_toggles(self):
        """
        Muda o comportamento dos toggles para um tipo de switch.
        """

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

    def control_mode(self):
        """
        Envia o modo de calculo, se os parametros indicados
        são trifásicos ou monofáscios
        """
        self.check_toggles()
        self.controller.set_mode(
            "trifasico" if self.ids.trifasico.state == "down" else "monofasico"
        )

    def value_setter(self, instance, focus, kw, value: float | None):
        """
        Generic caller for atribute setter.
        """
        if focus:
            return
        if kw == "_FP":
            self.controller.filter_TextInput(
                instance, kw, value, lower_limit=0, upper_limit=1
            )
            return
        if kw in ["_P", "_Q"]:
            upper = (
                float(self.ids.PotenciaAparente.text)
                if self.ids.PotenciaAparente.text
                else None
            )
            if upper is not None:
                self.controller.filter_TextInput(
                    instance, kw, value, lower_limit=0, upper_limit=upper
                )
                return
        self.controller.filter_TextInput(instance, kw, value, lower_limit=0)
        return

    def clear_button_signal(self):
        self.controller.clear_all()

    def model_is_changed(self, attribute, value):
        """
        The method is called when the model changes.
        Requests and displays the new values.
        """
        for element in self.walk():
            if not isinstance(element, TextInput):
                continue
            element: TextInput
            if element.name == attribute:
                element.text = str(round(value, 2) if value else "")


Builder.load_file(os.path.join(os.path.dirname(__file__), "uidesign.kv"))
