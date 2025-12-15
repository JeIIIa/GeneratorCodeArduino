import sys
from PySide6.QtWidgets import QApplication
from gui import SensorGenerator
from controller import CodeController


def main():
    app = QApplication(sys.argv)
    controller = CodeController()
    window = SensorGenerator(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()