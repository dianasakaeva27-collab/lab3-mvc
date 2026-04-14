import json
import os

class Model:
    """Модель хранит три числа A, B, C и обеспечивает правило A <= B <= C."""

    def __init__(self):
        self._a = 10
        self._b = 50
        self._c = 90
        self._observers = []

    def add_observer(self, observer):
        """Добавляет наблюдателя (например, View)."""
        self._observers.append(observer)

    def _notify(self):
        """Уведомляет всех наблюдателей об изменении модели."""
        for observer in self._observers:
            observer()

    def get_a(self): return self._a
    def get_b(self): return self._b
    def get_c(self): return self._c

    # ===== РАЗРЕШАЮЩЕЕ ПОВЕДЕНИЕ ДЛЯ A =====
    def set_a(self, value):
        """Устанавливает A. Если A > B, то B подтягивается. Если B > C, то C подтягивается."""
        value = max(0, min(100, value))
        old_a = self._a
        self._a = value

        if self._a > self._b:
            self._b = self._a
        if self._b > self._c:
            self._c = self._b

        if self._a != old_a:
            self._notify()

    # ===== ОГРАНИЧИВАЮЩЕЕ ПОВЕДЕНИЕ ДЛЯ B =====
    def set_b(self, value):
        """Устанавливает B, ограничивая его между A и C."""
        value = max(0, min(100, value))
        old_b = self._b

        # B не может быть меньше A и не может быть больше C
        self._b = max(self._a, min(self._c, value))

        if self._b != old_b:
            self._notify()

    # ===== РАЗРЕШАЮЩЕЕ ПОВЕДЕНИЕ ДЛЯ C =====
    def set_c(self, value):
        """Устанавливает C. Если C < B, то B подтягивается. Если B < A, то A подтягивается."""
        value = max(0, min(100, value))
        old_c = self._c
        self._c = value

        if self._c < self._b:
            self._b = self._c
        if self._b < self._a:
            self._a = self._b

        if self._c != old_c:
            self._notify()

    # ===== СОХРАНЕНИЕ И ЗАГРУЗКА =====
    def save(self, filename="data.json"):
        """Сохраняет значения в JSON файл."""
        data = {"a": self._a, "b": self._b, "c": self._c}
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename="data.json"):
        """Загружает значения из JSON файла."""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self._a = data.get("a", 10)
                self._b = data.get("b", 50)
                self._c = data.get("c", 90)
                self._notify()