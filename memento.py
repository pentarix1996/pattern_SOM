class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Originator:
    def __init__(self, state):
        self._state = state

    def set_state(self, state):
        print(f"Estado actual: {state}")
        self._state = state

    def save_to_memento(self):
        return Memento(self._state)

    def restore(self, memento: Memento):
        self._state = memento.get_state()
        print(f"Estado restaurado: {self._state}")


class Caretaker:
    def __init__(self):
        self._mementos = []

    def add_memento(self, memento):
        self._mementos.append(memento)

    def get_memento(self):
        if self._mementos:
            return self._mementos[-1]


originator = Originator("Estado inicial")
caretaker = Caretaker()

print(originator._state)
caretaker.add_memento(originator.save_to_memento())
originator.set_state("Nuevo Estado")
originator.restore(caretaker.get_memento())
