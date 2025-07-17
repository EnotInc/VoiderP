from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog
from sources.styles import apply_theme

from core.file_manager import FileManager
from core.text_buffer import TextBuffer

from ui.editor import TextEditor
from ui.file_tree import TreeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_menu()

        self.buffer = TextBuffer()
        self.file_manager = FileManager(self.buffer) 
        
        self.editor = TextEditor(self.buffer)
        self.tree_view = TreeView(self.file_manager)

        #self.tree_view.doubleClicked.connect(self._file_clicked)
        self.tree_view.clicked.connect(self._file_clicked)

        splitter = QSplitter()
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.editor)

        splitter.setSizes([248, 1000])

        self.setCentralWidget(splitter)
        self.resize(1000, 600)
        self.setMinimumSize(400, 300)

        apply_theme(self, 'dark')
 
 
    def _center_of_monitor(self):

        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft)


    def create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self._on_load)

        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self._on_save)
    
        view_menu = menu.addMenu("View")
        theme_menu = view_menu.addMenu('Theme')
        
        light = theme_menu.addAction("Light")
        light.triggered.connect(lambda: apply_theme(self, 'light'))
        dark = theme_menu.addAction("Dark")
        dark.triggered.connect(lambda: apply_theme(self, 'dark'))
        console = theme_menu.addAction("Console")
        console.triggered.connect(lambda: apply_theme(self, 'console'))


    def _file_clicked(self, index):
        self.tree_view.load_file(index)
        self.editor._sync_with_buffer()

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self.file_manager.load_file(path)
            self.editor._sync_with_buffer()
        
    def _on_save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file")
        if path:
            if self.file_manager.save_file(path):
                self.editor._sync_with_buffer()
