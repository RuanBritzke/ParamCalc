from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from typing import Literal

from matplotlib.dviread import Box

Vertical = Literal["vertical"]
Horizontal = Literal["horizontal"]


class IteractiveCreation(BoxLayout):
    def __init__(self, **kw):
        super(IteractiveCreation, self).__init__(**kw)
        self.orientation = "vertical"
        self.create_many_ToggleButtons(list(range(10)), "first", "horizontal"),
        self.create_many_buttons(list(range(10)), "vertical"),

    def create_many_buttons(
        self, texts: list | str, direction: Vertical | Horizontal = "horizontal"
    ):
        box1 = BoxLayout(orientation=direction)
        for name in texts:
            btn = Button(text=str(name))
            box1.add_widget(btn)
        self.add_widget(box1)

    def create_many_ToggleButtons(
        self, texts: list | str, grouping: str, direction: Vertical | Horizontal
    ):
        box2 = BoxLayout(orientation=direction)
        for name in texts:
            tgbtn = ToggleButton(text=str(name), group=grouping)
            box2.add_widget(tgbtn)
        self.add_widget(box2)


class MainApp(App):
    def build(self):
        return IteractiveCreation()


MainApp().run()
