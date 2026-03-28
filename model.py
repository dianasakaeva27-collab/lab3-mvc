import json
import os

class Model:
    def __init__(self):
        self._a = 10
        self._b = 50
        self._c = 90
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer()

    def get_a(self): return self._a
    def get_b(self): return self._b
    def get_c(self): return self._c

    def set_a(self, value):
        value = max(0, min(100, value))
        old_a = self._a
        self._a = value
        if self._a > self._b:
            self._b = self._a
        if self._b > self._c:
            self._c = self._b
        if self._a != old_a:
            self._notify()

    def set_b(self, value):
        value = max(0, min(100, value))
        old_b = self._b
        self._b = max(self._a, min(self._c, value))
        if self._b != old_b:
            self._notify()

    def set_c(self, value):
        value = max(0, min(100, value))
        old_c = self._c
        self._c = value
        if self._c < self._b:
            self._b = self._c
        if self._b < self._a:
            self._a = self._b
        if self._c != old_c:
            self._notify()

    def save(self, filename="data.json"):
        data = {"a": self._a, "b": self._b, "c": self._c}
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename="data.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self._a = data.get("a", 10)
                self._b = data.get("b", 50)
                self._c = data.get("c", 90)
                self._notify()