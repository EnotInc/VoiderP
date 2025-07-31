from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt

from sources.themes.styler import Styler

from core.file_manager import FileManager
from core.text_buffer import TextBuffer

from ui.editor.editor import TextEditor
from ui.editor.terminal import Terminal

from ui.main_window.file_tree import TreeView
from ui.main_window.label import Title
from ui.main_window.menu_bar import CustomMenu
from ui.main_window.preferences import Preferences
from ui.main_window.hello_page import Voider


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.styler = Styler(config)
        self.buffer = TextBuffer()
        self.file_manager = FileManager(config, self.buffer) 

        self.settings = Preferences(self.config)
        
        self.editor = TextEditor(self.config, self.buffer)
        self.terminal = Terminal()

        self.voider = Voider()
        self.title = Title()
        self.title.rename_trigger.connect(self._name_changed)
        self.tree_view = TreeView(self.config, self.file_manager)
        self.menu_bar = CustomMenu()
        self.setMenuBar(self.menu_bar)

        self.tree_view.doubleClicked.connect(self._file_clicked)

        self.main_splitter = QSplitter()
        self.editor_splitter = QSplitter(Qt.Orientation.Vertical)
        self.page = QStackedWidget()

        self.editor_splitter.addWidget(self.editor)
        self.editor_splitter.addWidget(self.terminal)
        self.editor_splitter.setSizes([800, 180 * self.config.show_terminal])

        work_space_widget = QWidget()
        self.work_space = QVBoxLayout()
        self.work_space.addWidget(self.title)
        self.work_space.addWidget(self.editor_splitter)
        work_space_widget.setLayout(self.work_space)

        self.page.addWidget(self.voider)
        self.page.addWidget(work_space_widget)

        self.main_splitter.addWidget(self.tree_view)
        self.main_splitter.addWidget(self.page)
        self.main_splitter.setSizes([384, 1000])

        self.editor_splitter.splitterMoved.connect(self._splitter_moved)

        self.setCentralWidget(self.main_splitter)
        self.setMinimumSize(400, 300) 

        self.menu_bar.theme_trigger.connect(self._apply_theme)
        self.menu_bar.open_trigger.connect(self._on_load)
        self.menu_bar.open_folder.connect(self._on_open_folder)
        self.menu_bar.save_trigger.connect(self._on_save)
        self.menu_bar.save_as_trigger.connect(self._on_save_as)
        self.menu_bar.purge_trigger.connect(self._on_purge_editor)
        self.menu_bar.terminal_trigger.connect(self._on_terminal)
        self.menu_bar.preferences.connect(self._on_preferences)

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
        self._apply_theme(self.styler.current_theme)
        self.title.set_title(self.file_manager.current_file)
        self.page.setCurrentIndex(1)

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self._apply_theme(self.styler.current_theme)
            self.file_manager.load_file(path)
            self.editor._sync_with_buffer()
            self.page.setCurrentIndex(1)
    
    def _on_open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if path:
            self.tree_view.open_folder(path) 
            self._on_purge_editor()
            self.page.setCurrentIndex(1)
        
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
        self.page.setCurrentIndex(0)

    def _name_changed(self):
        self.file_manager.rename_file(self.title.text())

    def _splitter_moved(self):
        self.config.show_terminal = self.editor_splitter.sizes()[1] > 10

    def _on_terminal(self):
        self.config.show_terminal = not self.config.show_terminal
        self.editor_splitter.setSizes([800, 180 * self.config.show_terminal])

    def _on_preferences(self):
        self.settings.exec()
        if self.settings.close():
            self.editor._apply_settings()
            self._apply_theme(self.styler.current_theme)

    def setup_work_space(self):
        self.file_manager.load_file(self.config.last_file)
        self.tree_view.open_folder(self.config.root_path)
        self.title.set_title(self.file_manager.current_file)

        if self.file_manager.current_file == "":
            self.page.setCurrentIndex(0)
        else:
            self.page.setCurrentIndex(1)

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
        if self.config.auto_save and self.buffer.changed:
            self._on_save()
        
        self.config.last_file = self.file_manager.current_file
        self.config.maximized = self.isMaximized()
        self.config.window_w = self.width()
        self.config.window_h = self.height()
           
        self.config.save_config()
        event.accept()