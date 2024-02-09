import attr
import logging

from typing import Any
from abc import ABC, abstractmethod


@attr.s(auto_attribs=True)
class SystemStrategy(ABC):

    config: dict[str, Any] = attr.ib(factory=dict)

    @abstractmethod
    def apply_configuration(self, config: dict[str, Any]):
        raise NotImplementedError()


class Observer(ABC):

    @abstractmethod
    def update(self, system_config: dict[str, Any]):
        raise NotImplementedError()


class AuditElement(Observer):

    def update(self, system_config: dict[str, Any]):
        print("Se están guardando logs sobre la configuración....")
        logging.info("Se aplicó una configuración:")
        for key, element in system_config.items():
            logging.info("Configuración: %s, Valor: %s", key, element)


class ClientElement(Observer):

    def update(self, system_config: dict[str, Any]):
        print("Mandando configuración a una api de terceros....")


@attr.s(auto_attribs=True)
class SystemStrategyA(SystemStrategy):

    def apply_configuration(self, config: dict[str, Any]):
        self.config.update(config)
        print("Aplicando configuración para el Sistema A")
        return self.config


@attr.s(auto_attribs=True)
class SystemStrategyB(SystemStrategy):

    def apply_configuration(self, config: dict[str, Any]):
        self.config.update(config)
        print("Aplicando configuración para el Sistema B")
        return self.config


class Application:
    def __init__(self, system: SystemStrategy):
        self.system = system
        self._observers = []

    def set_system(self, system: SystemStrategy):
        self.system = system

    def apply_configuration(self, key: str, value: str):
        config = {key: value}
        result = self.system.apply_configuration(config)
        self._notify_observers(result)

    def add_observer(self, observer: Observer):
        print(f"Añadiendo observador: {observer.__class__.__name__}")
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def _notify_observers(self, config: dict[str, Any]):
        for observer in self._observers:
            observer.update(config)



def select_system() -> str:
    user_input = input("Seleccione un sistema (A o B): ")

    while user_input not in ["A", "B", "e"]:
        user_input = input("Solo puede seleccionar A o B")

    return user_input


def input_menu() -> str:
    user_input = input("\nQue desea hacer?\n1. Seleccionar un sistema.\n"
                       "2. Añadir una configuración al sistema\n"
                       "3. Ver configuración del sistema.\n4. Salir\n>>> ")

    while user_input not in ["1", "2", "3", "4"]:
        user_input = input("Solo puede seleccionar 1, 2, 3 o 4 (salir): ")

    return user_input

switcher = {
    "A": SystemStrategyA(),
    "B": SystemStrategyB(),
}

system_input = select_system()
system = switcher[system_input]
app = Application(system)
observer_a = AuditElement()
observer_b = ClientElement()
app.add_observer(observer_a)
app.add_observer(observer_b)
user_input = input_menu()

while user_input != "4":
    if user_input == "1":
        system_input = select_system()
        system = switcher[system_input]
        app.set_system(system)
    elif user_input == "2":
        key = input("\nNombre de la configuración: ")
        value = input("Valor de la configuración: ")
        app.apply_configuration(key, value)
        pass
    elif user_input == "3":
        print(f"\nSistema actual: {app.system.__class__.__name__}")
        print(app.system.config)
    user_input = input_menu()
