import attr
import logging

from typing import Any
from copy import deepcopy
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


class SystemStrategyA(SystemStrategy):

    def apply_configuration(self, config: dict[str, Any]):
        self.config.update(config)
        print("Aplicando configuración para el Sistema A")
        return self.config


class SystemStrategyB(SystemStrategy):

    def apply_configuration(self, config: dict[str, Any]):
        self.config.update(config)
        print("Aplicando configuración para el Sistema B")
        return self.config


class Memento:

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config


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
    
    def save_config_state(self):
        return Memento(deepcopy(self.system.config))

    def restore(self, memento: Memento):
        self.system.config = memento.config
        print(f"Configuración restaurada: {self.system.config}")


class SnapshotSystem:
    def __init__(self, originator: Application) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        print("\nGuardando configuración...\n")
        self._mementos.append(self._originator.save_config_state())

    def undo(self) -> None:
        if not self._mementos:
            print("No hay configuraciones para restaurar.")
            return

        memento = self._mementos.pop()
        print(f"Restaurando configuración: {id(memento)}")
        self._originator.restore(memento)

    def show_history(self) -> None:
        print("Lista de configuraciones guardadas:")
        for index, memento in enumerate(self._mementos):
            print(f"Snapshot nº{index}: {id(memento)}")


def select_system() -> str:
    user_input = input("Seleccione un sistema (A o B): ")

    while user_input not in ["A", "B", "e"]:
        user_input = input("Solo puede seleccionar A o B")

    return user_input


def input_menu() -> str:
    user_input = input("\nQue desea hacer?\n1. Seleccionar un sistema.\n"
                       "2. Añadir una configuración al sistema\n"
                       "3. Ver configuración del sistema.\n"
                       "4. Ver Snapshots del sistema.\n"
                       "5. Deshacer último cambio\n6. Salir\n>>> ")

    while user_input not in ["1", "2", "3", "4", "5", "6"]:
        user_input = input("Solo puede seleccionar 1, 2, 3, 4 o 5 o 6 (salir): ")

    return user_input

switcher = {
    "A": SystemStrategyA(),
    "B": SystemStrategyB(),
}


system_input = select_system()
system = switcher[system_input]

app = Application(system)

caretakers = {
    id(switcher["A"]): SnapshotSystem(app),
    id(switcher["B"]): SnapshotSystem(app),
}

observer_a = AuditElement()
observer_b = ClientElement()

app.add_observer(observer_a)
app.add_observer(observer_b)

user_input = input_menu()

while user_input != "6":
    if user_input == "1":
        system_input = select_system()
        system = switcher[system_input]
        app.set_system(system)
    elif user_input == "2":
        key = input("\nNombre de la configuración: ")
        value = input("Valor de la configuración: ")
        caretakers[id(system)].backup()
        app.apply_configuration(key, value)
        pass
    elif user_input == "3":
        print(f"\nSistema actual: {app.system.__class__.__name__}")
        print(app.system.config)
    elif user_input == "4":
        caretakers[id(system)].show_history()
    elif user_input == "5":
        caretakers[id(system)].undo()
    user_input = input_menu()
