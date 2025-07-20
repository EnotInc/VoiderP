from PyQt6.QtCore import Qt, QDir
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel


class CustomFileModel(QFileSystemModel):
    def __init__(self, tree_view=None):
        super().__init__()
        self.tree_view = tree_view

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DecorationRole:
           return None

        if role == Qt.ItemDataRole.DisplayRole:
            name = super().data(index, role)
            if self.isDir(index):
                if self.tree_view and self.tree_view.isExpanded(index):
                    return f"- {name}"
                return f"+ {name}"
            else:
                file_info = self.fileInfo(index)
                file_name = file_info.fileName()
                file_ext = file_info.suffix().lower()

                if file_name[0] == '.':
                    return f"[_] {file_name}"
                elif file_ext:
                    return f"[{file_ext}] {file_name}"
                return f"[_] {file_name}"

        return super().data(index, role)

class TreeView(QTreeView):
    def __init__(self, config, file_manager):
        super().__init__()

        self.file_manager = file_manager

        self.treemodel = CustomFileModel(self)
        self.treemodel.setRootPath(QDir.currentPath())
        self.setModel(self.treemodel)

        self.setStyleSheet("QTreeView::branch{image: none;}")

        self.setHeaderHidden(True)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def load_file(self, index):
        path = self.model().filePath(index)
        if path and not self.model().isDir(index):
            self.file_manager.load_file(path)