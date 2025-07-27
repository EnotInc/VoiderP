from PyQt6.Qsci import QsciLexerPython, QsciLexerCPP, QsciLexerJavaScript, QsciScintilla, QsciLexerMarkdown
from PyQt6.QtGui import QColor

import json

class Lexer(QsciScintilla):
    def __init__(self, config, editor):
        super().__init__()
        self.editor: QsciScintilla = editor
        self.config = config
        self.current_lexer = None

    def setup_lexer(self, theme=None, path=None):
        try:
            with open("sources/themes/colors.json") as t:
                if not theme:
                    themes = json.load(t)[self.config.theme]
                else:
                    themes = json.load(t)[theme]
            
            self.text_color = themes["lexer"]["@main_text"]
            self.comment = themes["lexer"]["@comment"]
            self.string = themes["lexer"]["@strings"]
            self.keywords = themes["lexer"]["@keywords"]
            self.number = themes["lexer"]["@number"]
            self.funcs = themes["lexer"]["@funcs"]

            if not path or path == "":
                parts = self.config.last_file.split('.')
            else:
                parts = path.split('.')
            ext = parts[len(parts)-1]

            lexer = None

            if ext in ("py", "pyw"):
                lexer = QsciLexerPython()
                self.editor.setLexer(lexer)
                self.current_lexer = lexer
                self.python()

            elif ext in ("cpp", "cc", "cxx", "h", "hxx"):
                lexer = QsciLexerCPP()
                self.editor.setLexer(lexer)
                self.current_lexer = lexer
                self.cpp()

            elif ext in ("js", "ts"):
                lexer = QsciLexerJavaScript()
                self.editor.setLexer(lexer)
                self.current_lexer = lexer
                self.javascript()
            
            else:
                lexer = QsciLexerMarkdown()
                self.editor.setLexer(lexer)
                self.current_lexer = lexer

        except Exception as ex:         
            print(f"Error at lexer.py: {ex}")

    def python(self):
        self.current_lexer.setColor(QColor(self.text_color))
        self.current_lexer.setColor(QColor(self.comment), QsciLexerPython.Comment)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.DoubleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.SingleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.TripleDoubleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.TripleSingleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.DoubleQuotedFString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerPython.SingleQuotedFString)
        self.current_lexer.setColor(QColor(self.keywords), QsciLexerPython.Keyword)
        self.current_lexer.setColor(QColor(self.number), QsciLexerPython.Number)
        self.current_lexer.setColor(QColor(self.funcs), QsciLexerPython.FunctionMethodName)
        self.current_lexer.setColor(QColor(self.funcs), QsciLexerPython.ClassName)

    def cpp(self):
        self.current_lexer.setColor(QColor(self.text_color))
        self.current_lexer.setColor(QColor(self.comment), QsciLexerCPP.Comment)
        self.current_lexer.setColor(QColor(self.comment), QsciLexerCPP.CommentLine)
        self.current_lexer.setColor(QColor(self.string), QsciLexerCPP.SingleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerCPP.DoubleQuotedString)
        self.current_lexer.setColor(QColor(self.keywords), QsciLexerCPP.Keyword)
        self.current_lexer.setColor(QColor(self.number), QsciLexerCPP.Number)
        self.current_lexer.setColor(QColor(self.funcs), QsciLexerCPP.GlobalClass)

    def javascript(self):
        self.current_lexer.setColor(QColor(self.text_color))
        self.current_lexer.setColor(QColor(self.comment), QsciLexerJavaScript.Comment)
        self.current_lexer.setColor(QColor(self.comment), QsciLexerJavaScript.CommentLine)
        self.current_lexer.setColor(QColor(self.string), QsciLexerJavaScript.SingleQuotedString)
        self.current_lexer.setColor(QColor(self.string), QsciLexerJavaScript.DoubleQuotedString)
        self.current_lexer.setColor(QColor(self.keywords), QsciLexerJavaScript.Keyword)
        self.current_lexer.setColor(QColor(self.number), QsciLexerJavaScript.Number)
        self.current_lexer.setColor(QColor(self.funcs), QsciLexerJavaScript.GlobalClass)