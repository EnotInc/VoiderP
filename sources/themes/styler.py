import json
from PyQt6.QtGui import QColor, QFont

class Styler:
    def __init__(self, config):
        self.config = config

    def apply_theme(self, main_window, theme_name):
        try:
            theme_file = "sources/themes/style.qss"
            with open(theme_file, "r") as s:
                _style = s.read()
            
            with open("sources/themes/colors.json") as t:
                themes = json.load(t)[theme_name]

            for var, value in themes.items():
                _style = _style.replace(var, value)

            _style = _style.replace("@font_size", f"{self.config.font_size}px")
            _style = _style.replace("@font_family", self.config.font_family)

            _paper = themes["@main_fg"]
            _color = themes["@text_color"]

            _font = QFont()
            _font.setFamily(self.config.font_family)
            _font.setPointSize(self.config.font_size)

            main_window.editor._lexer.setup_lexer()
            main_window.editor._lexer.current_lexer.setPaper(QColor(_paper))

            main_window.editor.setPaper(QColor(_paper))
            main_window.editor.setColor(QColor(_color))
            main_window.editor.setMarginsBackgroundColor(QColor(_paper))
            main_window.editor.setMarginsForegroundColor(QColor(_color))
            main_window.editor.setFont(_font)

            main_window.setStyleSheet(_style)
        except Exception as ex:
            print(f"ERROR ad styler.py{ex}")