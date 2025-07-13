from PyQt6.Qsci import QsciScintilla
from PyQt6.QtGui import QFont, QColor

class TextEditor(QsciScintilla):

    def __init__(self, text_buffer):
        super().__init__()

        self.buffer = text_buffer
        self._sync_with_buffer()

        self.textChanged.connect(self._on_text_changed)

        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginsBackgroundColor(QColor("#000000"))
        self.setMarginsForegroundColor(QColor("#ffffff"))
        
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, 2)
        self.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor("#ffffff"))
        self.setCaretLineBackgroundColor(QColor("#3A3A3A"))
        
        self.setCaretWidth(3)

        self.update_margin_width()
        self.linesChanged.connect(self.update_margin_width)
    
        self.setPaper(QColor("#000000"))
        self.setColor(QColor("#ffffff"))

        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

    def _sync_with_buffer(self):
        self.setText(self.buffer.text)

    def _on_text_changed(self):
        self.buffer.text = self.text()

    def update_margin_width(self):
        digits = len(str(self.lines()))
        self.setMarginWidth(0, "0" * (digits + 1))

    def showEvent(self, event):
        super().showEvent(event)
        self.update_margin_width()
