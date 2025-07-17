from PyQt6.QtWidgets import QMenuBar, QFileDialog
from PyQt6.QtCore import pyqtSignal

class CustomMenu(QMenuBar):
    open_trigger = pyqtSignal()
    save_trigger = pyqtSignal()
    theme_trigger = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.create_menu()

    def create_menu(self):
        file_menu = self.addMenu("File")

        file_menu.addAction("Open", self.open_trigger.emit)
        file_menu.addAction("Save", self.save_trigger.emit)
    
        view_menu = self.addMenu("View")
        theme_menu = view_menu.addMenu('Theme')
        
        theme_menu.addAction("Light", lambda: self.theme_trigger.emit("light"))
        theme_menu.addAction("Dark", lambda: self.theme_trigger.emit('dark'))
        theme_menu.addAction("Console", lambda: self.theme_trigger.emit('console'))