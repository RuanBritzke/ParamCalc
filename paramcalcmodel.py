from math import *


class ParamCalcModel:
    def __init__(self) -> None:
        self._mode = "monofasico"
        self._S = None
        self._P = None
        self._Q = None
        self._FP = None
        self._V = None
        self._I = None
        self._observers = []

    def evaluate(self) -> None:
        if self._mode == "monofasico":
            self._evaluate_fase()
            return
        self._evaluate_linha()

    def _evaluate_linha(self):
        if self._S is None:
            self.S_linha()
        if self._P is None:
            self.P_linha()
        if self._Q is None:
            self.Q_linha()
        if self._FP is None:
            self.FP()
        if self._V is None:
            self.V_linha()
        if self._I is None:
            self.I_linha()

    def _evaluate_fase(self):
        if self._S is None:
            self.S_fase()
        if self._P is None:
            self.P_fase()
        if self._Q is None:
            self.Q_fase()
        if self._FP is None:
            self.FP()
        if self._V is None:
            self.V_fase()
        if self._I is None:
            self.I_fase()

    def S_fase(self) -> float:
        if self._P is not None and self._Q is not None:
            self._S = sqrt(self._P**2 + self._Q**2)
        elif self._P is not None and self._FP is not None:
            self._S = self._P / self._FP
        elif self._Q is not None and self._FP is not None:
            self._S = self._Q / sqrt(1 - self._FP**2)
        elif self._V is not None and self._I is not None:
            self._S = self._V * self._I
        else:
            return
        self.notify_observer("_S", self._S)

    def P_fase(self) -> float:

        if self._S is not None and self._Q is not None:
            self._P = sqrt(self._S**2 - self._Q**2)
        elif self._S is not None and self._FP is not None:
            self._P = self._S * self._FP
        elif self._Q is not None and self._FP is not None:
            self._P = self._Q / sqrt(1 - self._FP**-2)
        elif self._FP is not None and self._V is not None and self._I is not None:
            self._P = self._V * self._I * self._FP
        else:
            return
        self.notify_observer("_P", self._P)

    def Q_fase(self) -> float:
        if self._S is not None and self._P is not None:
            self._Q = sqrt(self._S**2 - self._P**2)
        elif self._S is not None and self._FP is not None:
            self._Q = self._S * sqrt(1 - self._FP**2)
        elif self._P is not None and self._FP is not None:
            self._Q = self._P * sqrt(self._FP**-2 - 1)
        elif self._FP is not None and self._V is not None and self._I:
            self._Q = self._V * self._I * sqrt(1 - self._FP**2)
        else:
            return
        self.notify_observer("_Q", self._Q)

    def FP(self) -> float:
        if self._S is not None and self._P is not None:
            self._FP = self._P / self._S
        elif self._S is not None and self._Q is not None:
            self._FP = sqrt(1 - self._Q**2 / self._S**2)
        elif self._P is not None and self._Q is not None:
            self._FP = self._P / sqrt(self._P**2 + self._Q**2)
        else:
            return
        self.notify_observer("_FP", self._FP)

    def V_fase(self) -> float:
        if self._S is not None and self._I is not None:
            self._V = self._S / self._I
        elif self._P is not None and self._I is not None and self._FP is not None:
            self._V = self._P / (self._I * self._FP)
        elif self._Q is not None and self._I is not None and self._FP is not None:
            self._V - self._Q / (self._I * sqrt(1 - self._FP**2))
        else:
            return
        self.notify_observer("_V", self._V)

    def I_fase(self) -> float:
        if self._S is not None and self._V is not None:
            self._I = self._S / self._V
        elif self._P is not None and self._I is not None and self._FP is not None:
            self._I = self._P / (self._V * self._FP)
        elif self._Q is not None and self._I is not None and self._FP is not None:
            self._I - self._Q / (self._V * sqrt(1 - self._FP**2))
        else:
            return
        self.notify_observer("_I", self._I)

    def S_linha(self) -> float:
        if self._V is None or self._I is None:
            self.S_fase()
        else:
            self._S = sqrt(3) * self._V * self._I
        self.notify_observer("_S", self._S)

    def P_linha(self) -> float:
        if self._V is None or self._I is None or self._FP is None:
            self.P_fase()
        else:
            self._P = sqrt(3) * self._V * self._I * self._FP
        self.notify_observer("_P", self._P)

    def Q_linha(self) -> float:
        if self._V is None or self._I is None or self._FP is None:
            self.Q_fase()
        else:
            self._Q = sqrt(3) * self._V * self._I * sqrt(1 - self._FP**2)
        self.notify_observer("_Q", self._Q)

    def V_linha(self) -> float:
        if self._S is not None and self._I is not None:
            self._V = self._S / (sqrt(3) * self._I)
        elif self._P is not None and self._I is not None and self._FP is not None:
            self._V = self._P / (sqrt(3) * self._I * self._FP)
        elif self._Q is not None and self._I is not None and self._FP is not None:
            self._V - self._Q / (sqrt(3) * self._I * sqrt(1 - self._FP**2))
        else:
            return
        self.notify_observer("_V", self._V)

    def I_linha(self) -> float:
        if self._S is not None and self._V is not None:
            self._I = self._S / (sqrt(3) * self._V)
        elif self._P is not None and self._I is not None and self._FP is not None:
            self._I = self._P / (sqrt(3) * self._V * self._FP)
        elif self._Q is not None and self._I is not None and self._FP is not None:
            self._I - self._Q / (sqrt(3) * self._V * sqrt(1 - self._FP**2))
        else:
            return
        self.notify_observer("_I", self._I)

    def reset(self):
        for kw in self.__dict__:
            if kw in ["_mode", "_observers"]:
                continue
            self.__dict__[kw] = None

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observer.remove(observer)

    def notify_observer(self, attribute, value):
        for x in self._observers:
            x.model_is_changed(attribute, value)


class ElectricalEquations:
    pass
