from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog
from PyQt6.QtCore import Qt

from sources.themes.styler import Styler

from core.file_manager import FileManager
from core.text_buffer import TextBuffer

from ui.editor.editor import TextEditor
from ui.editor.terminal import Terminal

from ui.main_window.file_tree import TreeView
from ui.main_window.menu_bar import CustomMenu


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.styler = Styler(config)
        self.buffer = TextBuffer()
        self.file_manager = FileManager(config, self.buffer) 
        
        self.editor = TextEditor(self.config, self.buffer)
        self.terminal = Terminal()

        self.tree_view = TreeView(self.config, self.file_manager)
        self.menu_bar = CustomMenu()
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
        self.styler.apply_theme(self, theme_name)

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
        if self.file_manager.current_file == "":
            self._on_save_as()
        else:
            self.file_manager.save_file()
        self.editor._sync_with_buffer()

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file")
        if path:
            if self.file_manager.save_as_file(path):
                self.editor._sync_with_buffer()

    def _on_purge_editor(self):
        self.file_manager.purge_editor()
        self.editor._sync_with_buffer()
        self.buffer.changed = False

    def setup_work_space(self):
        self.file_manager.load_file(self.config.last_file)
        self.tree_view.open_folder(self.config.root_path)

        self.WindowW = self.config.window_w
        self.WindowH = self.config.window_h
        if self.config.maximized:
            self.showMaximized()
        else:
            self.resize(self.WindowW, self.WindowH)

        self.editor._sync_with_buffer()
        self.buffer.changed = False
        self._apply_theme(self.config.theme)

    def closeEvent(self, event):
        if self.buffer.changed:
            self._on_save()

        self.config.save_config()
        event.accept()