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

        self.setWindowTitle("A <= B <= C")
        self.setGeometry(200, 200, 550, 250)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Заголовок
        title_label = QLabel("A <= B <= C")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)

        # Буквы A, B, C
        letters_layout = QHBoxLayout()
        letters_layout.addWidget(QLabel("     A     "))
        letters_layout.addWidget(QLabel("     B     "))
        letters_layout.addWidget(QLabel("     C     "))
        main_layout.addLayout(letters_layout)

        # Поля ввода
        edits_layout = QHBoxLayout()
        self.a_edit = QLineEdit()
        self.b_edit = QLineEdit()
        self.c_edit = QLineEdit()
        for edit in [self.a_edit, self.b_edit, self.c_edit]:
            edit.setAlignment(Qt.AlignCenter)
            edits_layout.addWidget(edit)
        main_layout.addLayout(edits_layout)

        # Счётчики
        spins_layout = QHBoxLayout()
        self.a_spin = QSpinBox()
        self.b_spin = QSpinBox()
        self.c_spin = QSpinBox()
        for spin in [self.a_spin, self.b_spin, self.c_spin]:
            spin.setRange(0, 100)
            spin.setAlignment(Qt.AlignCenter)
            spins_layout.addWidget(spin)
        main_layout.addLayout(spins_layout)

        # Ползунки
        sliders_layout = QHBoxLayout()
        self.a_slider = QSlider(Qt.Horizontal)
        self.b_slider = QSlider(Qt.Horizontal)
        self.c_slider = QSlider(Qt.Horizontal)
        for slider in [self.a_slider, self.b_slider, self.c_slider]:
            slider.setRange(0, 100)
            sliders_layout.addWidget(slider)
        main_layout.addLayout(sliders_layout)

        # ===== ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        # A
        self.a_edit.textChanged.connect(lambda t: self._on_text_changed('a', t))
        self.a_spin.valueChanged.connect(self.model.set_a)
        self.a_slider.valueChanged.connect(self.model.set_a)

        # B (ВАЖНО! Проверь эти строки)
        self.b_edit.textChanged.connect(lambda t: self._on_text_changed('b', t))
        self.b_spin.valueChanged.connect(self.model.set_b)
        self.b_slider.valueChanged.connect(self.model.set_b)  # ← ЭТО САМОЕ ВАЖНОЕ

        # C
        self.c_edit.textChanged.connect(lambda t: self._on_text_changed('c', t))
        self.c_spin.valueChanged.connect(self.model.set_c)
        self.c_slider.valueChanged.connect(self.model.set_c)

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
        """Обновляет все элементы управления"""
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