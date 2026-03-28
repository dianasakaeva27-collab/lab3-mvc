import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSlider)
from PyQt5.QtCore import Qt
from model import Model


# ========== ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ ==========
class MainWindow(QMainWindow):
    """Главное окно приложения (View).
    Отображает три числа A, B, C в трёх разных типах элементов:
    - текстовое поле (QLineEdit)
    - счётчик (QSpinBox)
    - ползунок (QSlider)
    
    При изменении любого элемента вызывает соответствующий метод модели.
    Подписывается на уведомления модели для обновления интерфейса."""

    def __init__(self):
        """Конструктор главного окна.
        Создаёт модель, подписывается на её обновления,
        создаёт все элементы управления и настраивает связи."""
        super().__init__()
        
        # Создаём экземпляр модели
        self.model = Model()
        # Подписываемся на уведомления модели (метод update_ui будет вызываться при изменениях)
        self.model.add_observer(self.update_ui)

        # Настройка окна
        self.setWindowTitle("MVC: A ≤ B ≤ C")
        self.setGeometry(200, 200, 500, 300)   # x, y, ширина, высота

        # ===== СОЗДАНИЕ ЭЛЕМЕНТОВ УПРАВЛЕНИЯ =====
        
        # Центральный виджет и основной вертикальный layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # ----- БЛОК ДЛЯ ЧИСЛА A -----
        layout.addWidget(QLabel("A:"))
        a_layout = QHBoxLayout()
        self.a_edit = QLineEdit()           # текстовое поле
        self.a_spin = QSpinBox()            # счётчик
        self.a_slider = QSlider(Qt.Horizontal)   # ползунок
        a_layout.addWidget(self.a_edit)
        a_layout.addWidget(self.a_spin)
        a_layout.addWidget(self.a_slider)
        layout.addLayout(a_layout)

        # ----- БЛОК ДЛЯ ЧИСЛА B -----
        layout.addWidget(QLabel("B:"))
        b_layout = QHBoxLayout()
        self.b_edit = QLineEdit()
        self.b_spin = QSpinBox()
        self.b_slider = QSlider(Qt.Horizontal)
        b_layout.addWidget(self.b_edit)
        b_layout.addWidget(self.b_spin)
        b_layout.addWidget(self.b_slider)
        layout.addLayout(b_layout)

        # ----- БЛОК ДЛЯ ЧИСЛА C -----
        layout.addWidget(QLabel("C:"))
        c_layout = QHBoxLayout()
        self.c_edit = QLineEdit()
        self.c_spin = QSpinBox()
        self.c_slider = QSlider(Qt.Horizontal)
        c_layout.addWidget(self.c_edit)
        c_layout.addWidget(self.c_spin)
        c_layout.addWidget(self.c_slider)
        layout.addLayout(c_layout)

        # Настройка диапазонов для счётчиков и ползунков (от 0 до 100)
        for spin in [self.a_spin, self.b_spin, self.c_spin]:
            spin.setRange(0, 100)
        for slider in [self.a_slider, self.b_slider, self.c_slider]:
            slider.setRange(0, 100)

        # ===== ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        # При изменении текстового поля A
        self.a_edit.textChanged.connect(lambda t: self._on_text_changed('a', t))
        # При изменении счётчика A
        self.a_spin.valueChanged.connect(lambda v: self.model.set_a(v))
        # При изменении ползунка A
        self.a_slider.valueChanged.connect(lambda v: self.model.set_a(v))

        # Аналогично для B
        self.b_edit.textChanged.connect(lambda t: self._on_text_changed('b', t))
        self.b_spin.valueChanged.connect(lambda v: self.model.set_b(v))
        self.b_slider.valueChanged.connect(lambda v: self.model.set_b(v))

        # Аналогично для C
        self.c_edit.textChanged.connect(lambda t: self._on_text_changed('c', t))
        self.c_spin.valueChanged.connect(lambda v: self.model.set_c(v))
        self.c_slider.valueChanged.connect(lambda v: self.model.set_c(v))

        # Загружаем сохранённые значения из файла
        self.model.load()
        # Обновляем интерфейс в соответствии с загруженными значениями
        self.update_ui()

    def _on_text_changed(self, var, text):
        """Обработчик изменения текста в текстовом поле.
        Преобразует текст в число и передаёт в модель.
        Если текст не является числом (пустая строка или буквы), игнорируется."""
        try:
            value = int(text)
            if var == 'a':
                self.model.set_a(value)
            elif var == 'b':
                self.model.set_b(value)
            elif var == 'c':
                self.model.set_c(value)
        except:
            # Если текст нельзя преобразовать в число (например, пусто или буквы),
            # ничего не делаем
            pass

    def update_ui(self):
        """Обновляет все элементы управления в соответствии с текущими значениями модели.
        Вызывается моделью при любом изменении данных.
        Важно: перед обновлением блокируются сигналы, чтобы не возникало бесконечных циклов
        (изменение поля -> вызов модели -> обновление UI -> снова изменение поля...)."""
        
        # Блокируем сигналы всех элементов, чтобы при установке значений
        # не вызывались их обработчики и не создавалась бесконечная петля
        self.a_edit.blockSignals(True)
        self.a_spin.blockSignals(True)
        self.a_slider.blockSignals(True)
        self.b_edit.blockSignals(True)
        self.b_spin.blockSignals(True)
        self.b_slider.blockSignals(True)
        self.c_edit.blockSignals(True)
        self.c_spin.blockSignals(True)
        self.c_slider.blockSignals(True)

        # Устанавливаем значения из модели во все элементы
        # Число A
        self.a_edit.setText(str(self.model.get_a()))
        self.a_spin.setValue(self.model.get_a())
        self.a_slider.setValue(self.model.get_a())

        # Число B
        self.b_edit.setText(str(self.model.get_b()))
        self.b_spin.setValue(self.model.get_b())
        self.b_slider.setValue(self.model.get_b())

        # Число C
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
        """Обработчик закрытия окна.
        Сохраняет текущие значения модели в файл перед закрытием."""
        self.model.save()      # сохраняем данные
        event.accept()         # разрешаем закрытие окна


# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    """Запуск приложения."""
    app = QApplication(sys.argv)      # создаём объект приложения
    window = MainWindow()             # создаём главное окно
    window.show()                     # показываем окно
    sys.exit(app.exec_())             # запускаем цикл обработки событий
