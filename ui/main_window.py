from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog
from PyQt6.QtCore import Qt

from sources.themes.styler import Styler

from core.file_manager import FileManager
from core.text_buffer import TextBuffer

from ui.editor import TextEditor
from ui.file_tree import TreeView
from ui.menu_bar import CustomMenu
from ui.terminal import Terminal


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.styler = Styler(config)
        self.buffer = TextBuffer()
        self.file_manager = FileManager(config, self.buffer) 
        
        self.editor = TextEditor(self.config, self.buffer)
        self.tree_view = TreeView(self.config, self.file_manager)
        self.menu_bar = CustomMenu()
        self.terminal = Terminal()
        self.setMenuBar(self.menu_bar)

        self.tree_view.doubleClicked.connect(self._file_clicked)

        main_splitter = QSplitter()
        editor_splitter = QSplitter(Qt.Orientation.Vertical)

        editor_splitter.addWidget(self.editor)
        editor_splitter.addWidget(self.terminal)
        editor_splitter.setSizes([800, 180])

        main_splitter.addWidget(self.tree_view)
        main_splitter.addWidget(editor_splitter)
        main_splitter.setSizes([384, 1000])

        self.setCentralWidget(main_splitter)
        self.setMinimumSize(400, 300) 

        self.menu_bar.theme_trigger.connect(self._apply_theme)
        self.menu_bar.open_trigger.connect(self._on_load)
        self.menu_bar.open_folder.connect(self._on_open_folder)
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
        _style = self.styler.apply_theme(theme_name)
        self.setStyleSheet(_style)

    def _file_clicked(self, index):
        self.tree_view.load_file(index)
        self.editor._sync_with_buffer()

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self.file_manager.load_file(path)
            self.editor._sync_with_buffer()
    
    def _on_open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if path:
            self.tree_view.open_folder(path) 
        
    def _on_save(self):
        if self.file_manager.current_file != "" and self.buffer.changed:
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

    def setup_work_space(self):
        self.file_manager.load_file(self.config.config["files"]["LastFile"])
        self.tree_view.open_folder(self.config.config["files"]["RootPath"])

        self.WindowH = self.config.config["editor"]["WindowH"]
        self.WindowV = self.config.config["editor"]["WindowV"]
        if self.config.config["editor"]["Maximized"]:
            self.showMaximized()
        else:
            self.resize(self.WindowH, self.WindowV)

        self.editor._sync_with_buffer()
        self._apply_theme(self.config.config["editor"]["Theme"])
        self.editor.setCursorWidth(self.config.config["editor"]["Font"]["Size"]//2 + 1)

    def closeEvent(self, event):
        self.config.config["editor"]["Maximized"] = int(self.isMaximized())
        self.config.config["editor"]["WindowH"] = self.size().width()
        self.config.config["editor"]["WindowV"] = self.size().height()

        self.config.config["editor"]["Theme"] = self.styler.theme
        self.config.config["editor"]["Font"]["Family"] = self.styler.font_family
        self.config.config["editor"]["Font"]["Size"] = self.styler.font_size

        self.config.config["files"]["RootPath"] = self.file_manager.root_path
        self.config.config["files"]["LastFile"] = self.file_manager.current_file

        self._on_save()
        self.config.save_config()
        event.accept()