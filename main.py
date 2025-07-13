import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PyQt6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.setWindowTitle("Voider")
    window.setWindowIcon(QIcon("sources/voider_icon.ico"))
        
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()