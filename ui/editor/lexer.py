from PyQt6.Qsci import QsciLexerPython, QsciLexerCPP, QsciLexerJavaScript, QsciLexerMarkdown
from PyQt6.Qsci import QsciScintilla

class Lexer(QsciScintilla):
    def __init__(self, config, editor):
        super().__init__()
        self.editor: QsciScintilla = editor
        self.config = config
        self.current_lexer = None

    def setup_lexer(self, ext=None):
        if not ext:
            parts = self.config.last_file.split('.')
            ext = parts[len(parts)-1]

        lexer = None

        if ext in ("py", "pyw"):
            lexer = QsciLexerPython()
        elif ext in ("cpp", "cc", "cxx", "h", "hxx"):
            lexer = QsciLexerCPP()
        elif ext in ("js", "ts"):
            lexer = QsciLexerJavaScript()
        elif ext in ("md"):
            lexer = QsciLexerMarkdown()
        
        if lexer:
            self.editor.setLexer(lexer)
            self.current_lexer = lexer