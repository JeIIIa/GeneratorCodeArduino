from PySide6.QtWidgets import QMessageBox


class CodeController:
    def __init__(self):
        self.sensors = []
        self.sensor_types = ["Потенциометр", "Фоторезистор", "Датчик наклона", "Датчик вибрации"]
        self.pin_names = {
            "Потенциометр": "pinRes",
            "Фоторезистор": "pinPRes", 
            "Датчик наклона": "pinST",
            "Датчик вибрации": "pinSV"
        }
        self.available_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
        self.used_pins = []
        self.gui = None  
        
    def set_gui(self, gui):
        self.gui = gui
        
    def add_sensor(self):
        if not self.gui:
            return
            
        if len(self.sensors) >= 6:
            QMessageBox.warning(self.gui, "Ошибка", "Максимум можно добавить 6 датчиков!")
            return
            
        sensor_type = self.gui.sensor_type_combo.currentText()
        pin = self.gui.pin_combo.currentText()
        
        if pin in self.used_pins:
            QMessageBox.warning(self.gui, "Ошибка", f"Пин {pin} уже используется!")
            return
        
        sensor_data = {
            'type': sensor_type,
            'pin': pin,
            'name': self.pin_names[sensor_type] + str(len(self.sensors) + 1)
        }
        
        self.sensors.append(sensor_data)
        self.used_pins.append(pin)
        
        self.update_pin_combo()
        self.update_sensors_list()
        
    def update_pin_combo(self):
        if not self.gui:
            return
            
        available = [pin for pin in self.available_pins if pin not in self.used_pins]
        self.gui.pin_combo.clear()
        self.gui.pin_combo.addItems(available)
        self.gui.pins_info.setText(f"Доступно пинов: {len(available)}")
        
    def update_sensors_list(self):
        if not self.gui:
            return
            
        text = ""
        for i, sensor in enumerate(self.sensors, 1):
            text += f"{i}. {sensor['type']} -> {sensor['pin']} (имя: {sensor['name']})\n"
        self.gui.sensors_list.setText(text)
        
    def clear_sensors(self):
        if not self.gui:
            return
            
        self.sensors.clear()
        self.used_pins.clear()
        self.update_pin_combo()
        self.gui.sensors_list.clear()
        self.gui.code_output.clear()
        
    def generate_code(self):
        if not self.gui:
            return
            
        if not self.sensors:
            QMessageBox.warning(self.gui, "Ошибка", "Добавьте хотя бы один датчик!")
            return
            
        code = "// Сгенерированный код для Arduino\n"
        
        for sensor in self.sensors:
            code += f"const int {sensor['name']} = {sensor['pin']};\n"
        code += "\n"
        
        for sensor in self.sensors:
            code += f"int val{sensor['name'][3:]} = 0; // Значение для {sensor['type']}\n"
        code += "\n"
        
        code += "void setup(){\n"
        code += "  Serial.begin(9600);\n"
        code += "}\n\n"
        
        code += "void loop(){\n"
        
        for sensor in self.sensors:
            var_name = f"val{sensor['name'][3:]}"
            code += f"  {var_name} = analogRead({sensor['name']});\n"
            
        code += "\n  // Вывод значений в монитор порта\n"
        for sensor in self.sensors:
            var_name = f"val{sensor['name'][3:]}"
            code += f"  Serial.print(\"{sensor['type']}: \");\n"
            code += f"  Serial.print({var_name});\n"
            code += "  Serial.print(\"\\t\");\n"
            
        code += "  Serial.println(); // Новая строка\n"
        code += "  delay(100);\n"
        code += "}\n"
        
        self.gui.code_output.setText(code)