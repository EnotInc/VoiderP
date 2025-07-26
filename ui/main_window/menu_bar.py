from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtCore import pyqtSignal

class CustomMenu(QMenuBar):
    open_trigger = pyqtSignal()
    open_folder = pyqtSignal()
    save_trigger = pyqtSignal()
    save_as_trigger = pyqtSignal()
    theme_trigger = pyqtSignal(str)
    purge_trigger = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.create_menu()

    def create_menu(self):
        file_menu = self.addMenu("File")

        file_menu.addAction("Open File", self.open_trigger.emit)
        file_menu.addAction("Open Folder", self.open_folder.emit)
        file_menu.addSeparator()
        file_menu.addAction("Save", self.save_trigger.emit)
        file_menu.addAction("Save As", self.save_as_trigger.emit)
        file_menu.addSeparator()
        file_menu.addAction("<Preferences>")
        

        view_menu = self.addMenu("View")
        
        theme_menu = view_menu.addMenu('Theme')
        view_menu.addAction("Purge Editor", self.purge_trigger.emit)
        view_menu.addAction("<Search>")
        view_menu.addAction("<Command Pallete>")
        view_menu.addAction("<Terminal>")
        
        theme_menu.addAction("Light", lambda: self.theme_trigger.emit("light"))
        theme_menu.addAction("Dark", lambda: self.theme_trigger.emit('dark'))
        theme_menu.addAction("Console", lambda: self.theme_trigger.emit('console'))