import json

from PyQt6.Qsci import (QsciScintilla,
                        QsciLexerPython, QsciLexerCPP, QsciLexerJavaScript, QsciLexerMarkdown)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class TextEditor(QsciScintilla):

    def __init__(self, config, text_buffer):
        super().__init__()

        self.config = config

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

    #TODO move this to the new lexer.py file    
    def setup_lexer(self, _paper):
        lexer = None

        parts = self.config.last_file.split('.')
        ext = parts[len(parts)-1]

        if ext in ("py", "pyw"):
            lexer = QsciLexerPython()
        elif ext in ("cpp", "cc", "cxx", "h", "hxx"):
            lexer = QsciLexerCPP()
        elif ext in ("js", "ts"):
            lexer = QsciLexerJavaScript()
        elif ext in ("md"):
            lexer = QsciLexerMarkdown()
        
        if lexer:
            lexer.setPaper(QColor(_paper))
            self.setLexer(lexer)

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
    