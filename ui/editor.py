from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import Qt

class TextEditor(QPlainTextEdit):

    def __init__(self, config, text_buffer):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.buffer = text_buffer
        self._sync_with_buffer()

        self.textChanged.connect(self._on_text_changed) 

    def _sync_with_buffer(self):
        self.setPlainText(self.buffer.text)

    def _on_text_changed(self):
        self.buffer.text = self.toPlainText()
        self.buffer.changed = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return
        super().keyPressEvent(event)
    