import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSlider)
from PyQt5.QtCore import Qt
from model import Model


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.model.add_observer(self.update_ui)

        self.setWindowTitle("MVC: A <= B <= C")
        self.setGeometry(200, 200, 500, 300)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Блок A
        layout.addWidget(QLabel("A:"))
        a_layout = QHBoxLayout()
        self.a_edit = QLineEdit()
        self.a_spin = QSpinBox()
        self.a_slider = QSlider(Qt.Horizontal)
        a_layout.addWidget(self.a_edit)
        a_layout.addWidget(self.a_spin)
        a_layout.addWidget(self.a_slider)
        layout.addLayout(a_layout)

        # Блок B
        layout.addWidget(QLabel("B:"))
        b_layout = QHBoxLayout()
        self.b_edit = QLineEdit()
        self.b_spin = QSpinBox()
        self.b_slider = QSlider(Qt.Horizontal)
        b_layout.addWidget(self.b_edit)
        b_layout.addWidget(self.b_spin)
        b_layout.addWidget(self.b_slider)
        layout.addLayout(b_layout)

        # Блок C
        layout.addWidget(QLabel("C:"))
        c_layout = QHBoxLayout()
        self.c_edit = QLineEdit()
        self.c_spin = QSpinBox()
        self.c_slider = QSlider(Qt.Horizontal)
        c_layout.addWidget(self.c_edit)
        c_layout.addWidget(self.c_spin)
        c_layout.addWidget(self.c_slider)
        layout.addLayout(c_layout)

        # Настройка диапазонов
        for spin in [self.a_spin, self.b_spin, self.c_spin]:
            spin.setRange(0, 100)
        for slider in [self.a_slider, self.b_slider, self.c_slider]:
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
        # Блокируем сигналы, чтобы избежать зацикливания
        self.a_edit.blockSignals(True)
        self.a_spin.blockSignals(True)
        self.a_slider.blockSignals(True)
        self.b_edit.blockSignals(True)
        self.b_spin.blockSignals(True)
        self.b_slider.blockSignals(True)
        self.c_edit.blockSignals(True)
        self.c_spin.blockSignals(True)
        self.c_slider.blockSignals(True)

        # Устанавливаем значения
        self.a_edit.setText(str(self.model.get_a()))
        self.a_spin.setValue(self.model.get_a())
        self.a_slider.setValue(self.model.get_a())

        self.b_edit.setText(str(self.model.get_b()))
        self.b_spin.setValue(self.model.get_b())
        self.b_slider.setValue(self.model.get_b())

        self.c_edit.setText(str(self.model.get_c()))
        self.c_spin.setValue(self.model.get_c())
        self.c_slider.setValue(self.model.get_c())

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