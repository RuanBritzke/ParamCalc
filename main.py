from math import degrees, radians, acos, asin, atan, cos, isnan, sin, sqrt
# from cmath import 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    label_fabricante = StringProperty()

    def __init__(self, **kw):
        super(MainWindow, self).__init__(**kw)
        self.label_fabricante = "Fabricante"

    def listar_fabricantes(self):
        self.box_popup = BoxLayout(orientation="vertical")
        self.box_popup.add_widget(
            Button(text="ITB", on_release=self.selecionar_fabricante)
        )
        self.box_popup.add_widget(
            Button(text="Siemens", on_release=self.selecionar_fabricante)
        )
        self.box_popup.add_widget(
            Button(text="Toshiba", on_release=self.selecionar_fabricante)
        )
        self.box_popup.add_widget(
            Button(text="McGraw", on_release=self.selecionar_fabricante)
        )
        self.popup = Popup(
            title="",
            separator_height=0,
            content=self.box_popup,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        self.popup.open()

    def selecionar_fabricante(self, instance):
        self.popup.dismiss()
        self.label_fabricante = instance.text


class Calculadora(Screen):
    S = StringProperty("")
    P = StringProperty("")
    Q = StringProperty("")
    phi = StringProperty("")
    FP = StringProperty("")
    V = StringProperty("")
    I = StringProperty("")

    def __init__(self, **kw):
        super(Calculadora, self).__init__(**kw)
        self.S = self.P = self.Q = self.phi = self.FP = self.V = self.I = ""

    def salva_info(self):
        S = self.ids.potencia_aparente.text
        P = self.ids.potencia_ativa.text
        Q = self.ids.potencia_reativa.text
        phi = self.ids.angulo_de_fase.text
        FP = self.ids.fator_de_potencia.text
        V = self.ids.tensao.text
        I = self.ids.corrente.text

        if self.ids.monofasico.state == "down":
            self.calcular(
                S,
                P,
                Q,
                phi,
                FP,
                V,
                I,
            )
        elif self.ids.trifasico.state == "down":
            S = str(float(S) / 3) if S != "" else ""
            P = str(float(P) / 3) if P != "" else ""
            Q = str(float(Q) / 3) if Q != "" else ""
            V = str(float(V) / sqrt(3)) if V != "" else ""
            self.calcular(S, P, Q, phi, FP, V, I)

    def atualizar_resultados(
        self, S: str, P: str, Q: str, phi: str, FP: str, V: str, I: str
    ):

        if self.ids.monofasico.state == "down":
            self.S = S
            self.P = P
            self.Q = Q
            self.phi = phi
            self.FP = FP
            self.V = V
            self.I = I

        elif self.ids.trifasico.state == "down":
            self.S = str(round(float(S) * 3, 2)) if S != "" else ""
            self.P = str(round(float(P) * 3, 2)) if P != "" else ""
            self.Q = str(round(float(Q) * 3, 2)) if Q != "" else ""
            self.phi = phi
            self.FP = FP
            self.V = str(round(float(V) * sqrt(3), 2)) if V != "" else ""
            self.I = I
        pass

    def limpar(self):
        self.ids.potencia_aparente.text = ""
        self.ids.potencia_ativa.text = ""
        self.ids.potencia_reativa.text = ""
        self.ids.angulo_de_fase.text = ""
        self.ids.fator_de_potencia.text = ""
        self.ids.tensao.text = ""
        self.ids.corrente.text = ""

    def calcular(self, S, P, Q, phi, FP, V, I):

        new_S = self.calcular_S(S, P, Q, phi, FP, V, I)
        new_P = self.calcular_P(S, P, Q, phi, FP, V, I)
        new_Q = self.calcular_Q(S, P, Q, phi, FP, V, I)
        new_phi = self.calcular_phi(S, P, Q, phi, FP, V, I)
        new_FP = self.calcular_FP(S, P, Q, phi, FP, V, I)
        new_V = self.calcular_V(S, P, Q, phi, FP, V, I)
        new_I = self.calcular_I(S, P, Q, phi, FP, V, I)

        self.atualizar_resultados(new_S, new_P, new_Q, new_phi, new_FP, new_V, new_I)

    def calcular_S(self, S, P, Q, phi, FP, V, I):

        old_S = S
        if bool(P) * bool(Q):
            S = sqrt(float(P) ** 2 + float(Q) ** 2)
        elif bool(P) * bool(FP):
            S = float(P) / float(FP)
        elif bool(P) * bool(phi):
            if bool(cos(float(phi))):
                S = float(P) / cos(float(phi))
        elif bool(Q) * bool(phi):
            if bool(sin(radians(float(phi)))):
                S = float(Q) / sin(radians(float(phi)))
        elif bool(V) * bool(I):
            S = float(V) * float(I)
        else:
            return old_S
        return str(round(S, 2)) if not isnan(S) else old_S

    def calcular_P(self, S, P, Q, phi, FP, V, I):

        old_P = P

        if bool(S) * bool(Q):
            P = sqrt(float(S) ** 2 - float(Q) ** 2)
        elif bool(S) * bool(phi):
            if bool(cos(radians(float(phi)))):
                P = float(S) * cos(radians(float(phi)))
        elif bool(S) * bool(FP):
            P = float(S) * float(FP)
        elif bool(V) * bool(I) * bool(phi):
            if bool(cos(radians(float(phi)))):
                P = float(V) * float(I) * cos(radians(float(phi)))
        elif bool(V) * bool(I) * bool(FP):
            P = float(V) * float(I) * float(FP)
        else:
            return old_P
        return str(round(P, 2)) if not isnan(P) else old_P

    def calcular_Q(self, S, P, Q, phi, FP, V, I):

        old_Q = Q
        if bool(S) * bool(P):
            Q = sqrt(float(S) ** 2 - float(P) ** 2)
        elif bool(S) * bool(phi):
            Q = float(S) * sin(radians(float(phi)))
        elif bool(V) * bool(I) * bool(phi):
            if bool(sin(radians(float(phi)))):
                Q = float(V) * float(I) * sin(radians(float(phi)))
        else:
            return old_Q
        return str(round(Q, 2)) if not isnan(Q) else old_Q

    def calcular_phi(self, S, P, Q, phi, FP, V, I):

        old_phi = phi
        if bool(Q) * bool(P):
            phi = atan(float(Q) / float(P))
        elif bool(S) * bool(P):
            phi = acos(float(P) / float(S))
        elif bool(S) * bool(Q):
            phi = asin(float(Q) / float(S))
        elif bool(FP):
            phi = acos(float(FP))
        else:
            return old_phi
        return str(round(degrees(phi.real), 2)) if not isnan(phi) else old_phi

    def calcular_FP(self, S, P, Q, phi, FP, V, I):

        old_FP = FP
        if bool(phi):
            FP = cos(float(radians(float(phi))))
        elif bool(P) * bool(S):
            FP = float(P) / float(S)
        else:
            return old_FP
        return str(round(FP, 2)) if not isnan(FP) else old_FP

    def calcular_V(self, S, P, Q, phi, FP, V, I):

        old_V = V
        if bool(I):
            if bool(S):
                V = float(S) / float(I)
            elif bool(P) * bool(phi):
                V = float(P) / (float(I) * cos(float(phi)))
            elif bool(P) * bool(FP):
                V = float(P) / (float(I) * float(FP))
            elif bool(Q) * bool(phi):
                V = float(Q) / (float(I) * sin(float(phi)))
            else:
                return old_V
        else:
            return old_V
        return str(round(V, 2)) if not isnan(V) else old_V

    def calcular_I(self, S, P, Q, phi, FP, V, I):
        # I = S/V
        # I = P/(V*cos(phi))
        # I = P/(V*FP)
        # I = Q/(V*sin(phi))
        old_I = I
        if bool(V):
            if bool(S):
                I = float(S) / float(V)
            elif bool(P) * bool(phi):
                I = float(P) / (float(V) * cos(float(phi)))
            elif bool(P) * bool(FP):
                I = float(P) / (float(V) * float(FP))
            elif bool(Q) * bool(phi):
                I = float(Q) / (float(V) * sin(float(phi)))
            else:
                return old_I
        else:
            return old_I
        return str(round(I, 2)) if not isnan(I) else old_I


class MainApp(App):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    MainApp().run()
