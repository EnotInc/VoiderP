from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui.editor.lexer import Lexer

class TextEditor(QsciScintilla):

    def __init__(self, config, text_buffer):
        super().__init__()

        self.config = config
        self._lexer = Lexer(self.config, self)

        self.buffer = text_buffer
        self._sync_with_buffer()

        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, self.config.cursor_style)
        self.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor("#FFFFFF"))
        self.setCaretLineBackgroundColor(QColor("#3A3A3A"))

        self.setWrapMode(QsciScintilla.WrapMode.WrapWord)

        self.setCaretWidth(3)

        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        digits = 4
        self.setMarginWidth(0, " " * (digits+1) +"9"*digits )

        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)

        self.textChanged.connect(self._on_text_changed) 

    def _sync_with_buffer(self):
        self.setText(self.buffer.text)

    def _on_text_changed(self):
        self.buffer.text = self.text()
        self.buffer.changed = True

    def _keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return
        super().keyPressEvent(event)
    