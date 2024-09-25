from logic_old.logic_codechrono import CodeChronoApp
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = CodeChronoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
