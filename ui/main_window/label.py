from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class Title(QLabel):
    def __init__(self):
        super().__init__()
        self._text = "Undefined"
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(self._text)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        parts = value.split('/')
        name = parts[len(parts) - 1]
        self._text = name
        self.setText(name)