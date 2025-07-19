from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog

from sources.themes.styler import apply_theme
from sources.settings import ConfigManager

from core.file_manager import FileManager
from core.text_buffer import TextBuffer

from ui.editor import TextEditor
from ui.file_tree import TreeView
from ui.menu_bar import CustomMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()

        self.buffer = TextBuffer()
        self.file_manager = FileManager(self.buffer) 
        
        self.editor = TextEditor(self.buffer)
        self.tree_view = TreeView(self.file_manager)
        self.menu_bar = CustomMenu()
        self.setMenuBar(self.menu_bar)

        self.tree_view.doubleClicked.connect(self._file_clicked)

        splitter = QSplitter()
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.editor)

        splitter.setSizes([512, 1000])

        self.setCentralWidget(splitter)
        self.resize(1000, 600)
        self.setMinimumSize(400, 300) 

        self.menu_bar.theme_trigger.connect(self._apply_theme)
        self.menu_bar.open_trigger.connect(self._on_load)
        self.menu_bar.save_trigger.connect(self._on_save)
        self.menu_bar.save_as_trigger.connect(self._on_save_as)
        self.menu_bar.purge_trigger.connect(self._on_purge_editor)

        self.setup_work_space()
 
    def _center_of_monitor(self):

        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft)

    def _apply_theme(self, theme_name):
        _style = apply_theme(theme_name)
        self.setStyleSheet(_style)
        self.config.config["editor"]["Theme"] = theme_name

    def _file_clicked(self, index):
        self.tree_view.load_file(index)
        self.editor._sync_with_buffer()
        self.config.config["files"]["LastFile"] = self.file_manager.current_file

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self.file_manager.load_file(path)
            self.editor._sync_with_buffer()
            self.config.config["files"]["LastFile"] = self.file_manager.current_file
        
    def _on_save(self):
        if self.file_manager.current_file != "":
             self.file_manager.save_file()
        else:
            self._on_save_as()
        self.editor._sync_with_buffer()

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file")
        if path:
            if self.file_manager.save_as_file(path):
                self.editor._sync_with_buffer()

    def _on_purge_editor(self):
        self.file_manager.purge_editor()
        self.editor._sync_with_buffer()
        self.config.config["files"]["LastFile"] = ""

    def setup_work_space(self):
        self.file_manager.load_file(self.config.config["files"]["LastFile"])
        self.editor._sync_with_buffer()
        self._apply_theme(self.config.config["editor"]["Theme"])

    def closeEvent(self, event):
        self.file_manager.save_file()
        self.config.save_config()
        event.accept()