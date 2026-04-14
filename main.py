import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSlider)
from PyQt5.QtCore import Qt
from model import Model


class LimitedSlider(QSlider):
    """Ползунок, который останавливается на границах [min_limit, max_limit]."""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self._min_limit = 0
        self._max_limit = 100
        self.setRange(0, 100)
    
    def setLimits(self, min_val, max_val):
        """Устанавливает границы, за которые нельзя выходить."""
        self._min_limit = min_val
        self._max_limit = max_val
    
    def sliderChange(self, change):
        """Переопределяем метод изменения положения ползунка."""
        if change == self.SliderValueChange:
            value = self.value()
            # Ограничиваем значение
            if value < self._min_limit:
                self.setValue(self._min_limit)
            elif value > self._max_limit:
                self.setValue(self._max_limit)
        super().sliderChange(change)


class LimitedSpinBox(QSpinBox):
    """Счётчик, который останавливается на границах [min_limit, max_limit]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._min_limit = 0
        self._max_limit = 100
        self.setRange(0, 100)
    
    def setLimits(self, min_val, max_val):
        """Устанавливает границы, за которые нельзя выходить."""
        self._min_limit = min_val
        self._max_limit = max_val
    
    def fixup(self, input_str):
        """Вызывается при вводе некорректного значения."""
        try:
            val = int(input_str)
            if val < self._min_limit:
                self.setValue(self._min_limit)
            elif val > self._max_limit:
                self.setValue(self._max_limit)
        except:
            pass
        super().fixup(input_str)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.model.add_observer(self.update_ui)

        self.setWindowTitle("Form1")
        self.setGeometry(200, 200, 500, 250)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Заголовок
        title_label = QLabel("A <= B <= C")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # ===== СТРОКА ДЛЯ A =====
        a_layout = QHBoxLayout()
        self.a_edit = QLineEdit()
        self.a_spin = QSpinBox()
        self.a_slider = QSlider(Qt.Horizontal)
        a_layout.addWidget(self.a_edit)
        a_layout.addWidget(self.a_spin)
        a_layout.addWidget(self.a_slider)
        main_layout.addLayout(a_layout)

        # ===== СТРОКА ДЛЯ B (с ограничивающими элементами) =====
        b_layout = QHBoxLayout()
        self.b_edit = QLineEdit()
        self.b_spin = LimitedSpinBox()
        self.b_slider = LimitedSlider(Qt.Horizontal)
        b_layout.addWidget(self.b_edit)
        b_layout.addWidget(self.b_spin)
        b_layout.addWidget(self.b_slider)
        main_layout.addLayout(b_layout)

        # ===== СТРОКА ДЛЯ C =====
        c_layout = QHBoxLayout()
        self.c_edit = QLineEdit()
        self.c_spin = QSpinBox()
        self.c_slider = QSlider(Qt.Horizontal)
        c_layout.addWidget(self.c_edit)
        c_layout.addWidget(self.c_spin)
        c_layout.addWidget(self.c_slider)
        main_layout.addLayout(c_layout)

        # Настройка диапазонов (ВСЕ ОТ 0 ДО 100)
        for spin in [self.a_spin, self.c_spin]:
            spin.setRange(0, 100)
        for slider in [self.a_slider, self.c_slider]:
            slider.setRange(0, 100)

        # Подключение сигналов
        self.a_edit.textChanged.connect(lambda t: self._on_text_changed('a', t))
        self.a_spin.valueChanged.connect(lambda v: self.model.set_a(v))
        self.a_slider.valueChanged.connect(lambda v: self.model.set_a(v))

        self.b_edit.textChanged.connect(lambda t: self._on_text_changed('b', t))
        self.b_spin.valueChanged.connect(lambda v: self.model.set_b(v))
        self.b_slider.valueChanged.connect(lambda v: self.model.set_b(v))

        self.c_edit.textChanged.connect(lambda t: self._on_text_changed('c', t))
        self.c_spin.valueChanged.connect(lambda v: self.model.set_c(v))
        self.c_slider.valueChanged.connect(lambda v: self.model.set_c(v))

        # Загрузка и обновление
        self.model.load()
        self.update_ui()

    def _on_text_changed(self, var, text):
        try:
            value = int(text)
            if var == 'a':
                self.model.set_a(value)
            elif var == 'b':
                self.model.set_b(value)
            elif var == 'c':
                self.model.set_c(value)
        except:
            pass

    def update_ui(self):
        # Блокируем сигналы
        self.a_edit.blockSignals(True)
        self.a_spin.blockSignals(True)
        self.a_slider.blockSignals(True)
        self.b_edit.blockSignals(True)
        self.b_spin.blockSignals(True)
        self.b_slider.blockSignals(True)
        self.c_edit.blockSignals(True)
        self.c_spin.blockSignals(True)
        self.c_slider.blockSignals(True)

        # Устанавливаем значения A и C
        self.a_edit.setText(str(self.model.get_a()))
        self.a_spin.setValue(self.model.get_a())
        self.a_slider.setValue(self.model.get_a())

        self.c_edit.setText(str(self.model.get_c()))
        self.c_spin.setValue(self.model.get_c())
        self.c_slider.setValue(self.model.get_c())

        # Устанавливаем ГРАНИЦЫ для B (а не диапазон!)
        min_b = self.model.get_a()
        max_b = self.model.get_c()
        self.b_spin.setLimits(min_b, max_b)
        self.b_slider.setLimits(min_b, max_b)

        # Устанавливаем значение B
        self.b_edit.setText(str(self.model.get_b()))
        self.b_spin.setValue(self.model.get_b())
        self.b_slider.setValue(self.model.get_b())

        # Разблокируем сигналы
        self.a_edit.blockSignals(False)
        self.a_spin.blockSignals(False)
        self.a_slider.blockSignals(False)
        self.b_edit.blockSignals(False)
        self.b_spin.blockSignals(False)
        self.b_slider.blockSignals(False)
        self.c_edit.blockSignals(False)
        self.c_spin.blockSignals(False)
        self.c_slider.blockSignals(False)

    def closeEvent(self, event):
        self.model.save()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())