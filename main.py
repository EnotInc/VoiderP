import sys
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from sources.settings import ConfigManager
from ui.main_window import MainWindow


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    config = ConfigManager()
    window = MainWindow(config)

    window.setWindowTitle("Voider")
    window.setWindowIcon(QIcon("sources/voider_icon.ico"))
    window.show()
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()