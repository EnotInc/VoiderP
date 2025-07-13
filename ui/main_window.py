from PyQt6.QtWidgets import QMainWindow, QSplitter, QFileDialog

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
        self.tree_view = TreeView()

        splitter = QSplitter()
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.editor)

        splitter.setSizes([248, 1000])

        self.setCentralWidget(splitter)
        self.resize(800, 600)
        self.setMinimumSize(400, 300)
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #000000;
                color: #ffffff;
            }
            QTreeView {
                background-color: #000000;
                color: #ffffff;
                border: none;
            }
            QTreeView::item:hover {
                background-color: #333333;
            }
            QTreeView::item:selected {
                background-color: #333333;
            }
            QSplitter::handle {
                width: 1px;
                background: #000000;
            }
            QSplitter::handle:hover {
                background: #333333; 
            }
        """)

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
