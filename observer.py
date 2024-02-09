class Observer:
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self):
        print(f"Recibido - {self.name}")


class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.update()

    def some_business_logic(self):
        print("Haciendo algo importante")
        self._notify_observers()


subject = Subject()
observer_a = Observer("A")
observer_b = Observer("B")
observer_c = Observer("C")
subject.add_observer(observer_a)
subject.add_observer(observer_c)
subject.some_business_logic()
