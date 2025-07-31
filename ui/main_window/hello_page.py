from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class Voider(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Oh hello there\n\n<(^-^)>")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)