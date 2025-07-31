import os
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal

class Title(QLineEdit):

    rename_trigger = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.returnPressed.connect(self.rename)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)
    
    def rename(self):
        self.rename_trigger.emit()
    
    def set_title(self, value):
        if value:
            name = os.path.basename(value)
            self.setText(name)