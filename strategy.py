from abc import ABC, abstractmethod


class SystemStrategy(ABC):
    @abstractmethod
    def apply_configuration(self):
        raise NotImplementedError()


class SystemStrategyA(SystemStrategy):
    def apply_configuration(self):
        return "Aplicando configuración para el Sistema A"


class SystemStrategyB(SystemStrategy):
    def apply_configuration(self):
        return "Aplicando configuración para el Sistema B"


class Application:
    def __init__(self, system: SystemStrategy):
        self.system = system

    def set_system(self, system: SystemStrategy):
        self.system = system

    def apply_configuration(self):
        return self.system.apply_configuration()


def select_system() -> str:
    user_input = input("Seleccione un sistema (A o B) o salir (e): ")

    while user_input not in ["A", "B", "e"]:
        user_input = input("Solo puede seleccionar A o B o salir (e): ")

    return user_input

switcher = {
    "A": SystemStrategyA,
    "B": SystemStrategyB,
}
user_input = select_system()

while user_input != "e":
    system = switcher[user_input]()
    app = Application(system)
    print(app.apply_configuration())
    user_input = select_system()
