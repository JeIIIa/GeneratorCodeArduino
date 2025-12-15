import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QPushButton, 
                               QSpinBox, QTextEdit, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from controller import CodeController


class SensorGenerator(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.set_gui(self) 
        
        self.setWindowTitle("Генератор кода Arduino")
        self.setWindowIcon(QIcon(r'Icons\home.svg'))
        self.setFixedSize(600, 700)
         
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
    
        # Группа для добавления датчиков
        sensor_group = QGroupBox("Добавить датчик")
        sensor_layout = QVBoxLayout()
        
        # Выбор типа датчика
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип датчика:"))
        self.sensor_type_combo = QComboBox()
        self.sensor_type_combo.addItems(["Потенциометр", "Фоторезистор", "Датчик наклона", "Датчик вибрации"])
        type_layout.addWidget(self.sensor_type_combo)
        sensor_layout.addLayout(type_layout)
        
        # Выбор пина
        pin_layout = QHBoxLayout()
        pin_layout.addWidget(QLabel("Аналоговый пин:"))
        self.pin_combo = QComboBox()
        self.pin_combo.addItems(self.controller.available_pins)
        pin_layout.addWidget(self.pin_combo)
        sensor_layout.addLayout(pin_layout)
        
        # Кнопка добавления
        self.add_button = QPushButton("Добавить датчик")
        self.add_button.setIcon(QIcon(r"Icons\add.svg"))
        self.add_button.clicked.connect(self.controller.add_sensor)
        sensor_layout.addWidget(self.add_button)
        
        # Информация о доступных пинах
        self.pins_info = QLabel(f"Доступно пинов: {len(self.controller.available_pins)}")
        sensor_layout.addWidget(self.pins_info)
        
        sensor_group.setLayout(sensor_layout)
        main_layout.addWidget(sensor_group)
        
        # Список добавленных датчиков
        self.sensors_list = QTextEdit()
        self.sensors_list.setReadOnly(True)
        self.sensors_list.setMaximumHeight(150)
        self.sensors_list.setPlaceholderText("Добавленные датчики появятся здесь...")
        main_layout.addWidget(QLabel("Добавленные датчики:"))
        main_layout.addWidget(self.sensors_list)
        
        # Кнопка очистки
        clear_button = QPushButton("Очистить все датчики")
        clear_button.setIcon(QIcon(r"Icons\delete.svg"))
        clear_button.clicked.connect(self.controller.clear_sensors)
        main_layout.addWidget(clear_button)
        
        # Генерация кода
        generate_button = QPushButton("Сгенерировать код Arduino")
        generate_button.setIcon(QIcon(r'Icons\check.svg'))
        generate_button.clicked.connect(self.controller.generate_code)
        main_layout.addWidget(generate_button)
        
        # Поле сгенерированного кода
        main_layout.addWidget(QLabel("Сгенерированный код:"))
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)
        self.code_output.setPlaceholderText("Здесь появится сгенерированный код...")
        main_layout.addWidget(self.code_output)