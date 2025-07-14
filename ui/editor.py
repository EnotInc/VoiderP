from PyQt6.QtWidgets import QPlainTextEdit 

class TextEditor(QPlainTextEdit):

    def __init__(self, text_buffer):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.buffer = text_buffer
        self._sync_with_buffer()

        self.textChanged.connect(self._on_text_changed) 

    def _sync_with_buffer(self):
        self.setPlainText(self.buffer.text)

    def _on_text_changed(self):
        self.buffer.text = self.toPlainText()

    def showEvent(self, event):
        super().showEvent(event)
