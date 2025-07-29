from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class Title(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)
        self.setReadOnly(True)
    
    @property
    def text(self):
        return super().text()
    
    @text.setter
    def text(self, value):
        parts = value.split('/')
        name = parts[len(parts) - 1]
        self.setText(name)