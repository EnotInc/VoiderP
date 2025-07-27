import json
from PyQt6.QtGui import QColor, QFont

class Styler:
    def __init__(self, config):
        self.config = config
        self.current_theme = self.config.config["editor"]["Theme"]

    def apply_theme(self, main_window, theme_name):
        try:
            self.current_theme = theme_name
            theme_file = "sources/themes/style.qss"
            with open(theme_file, "r") as s:
                _style = s.read()
            
            with open("sources/themes/colors.json") as t:
                themes = json.load(t)[theme_name]

            _style = _style.replace("@main_bg", themes["@main_bg"])
            _style = _style.replace("@main_fg", themes["@main_fg"])
            _style = _style.replace("@text_color", themes["@text_color"])
            _style = _style.replace("@hover", themes["@hover"])
            _style = _style.replace("@font_size", f"{self.config.font_size}px")
            _style = _style.replace("@font_family", self.config.font_family)

            _paper = themes["@main_fg"]
            _color = themes["@text_color"]

            _font = QFont(self.config.font_family)
            _font.setPointSize(self.config.font_size)

            current_file = main_window.file_manager.current_file 
            main_window.editor._lexer.setup_lexer(theme=theme_name, path=current_file)
            
            main_window.editor._lexer.current_lexer.setPaper(QColor(_paper))

            main_window.editor.setPaper(QColor(_paper))
            main_window.editor.setColor(QColor(_color))
            main_window.editor.setMarginsBackgroundColor(QColor(_paper))
            main_window.editor.setMarginsForegroundColor(QColor(_color))
            main_window.editor._lexer.current_lexer.setFont(_font)

            main_window.editor._lexer.setFont(_font)
            main_window.editor.setFont(_font)

            main_window.setStyleSheet(_style)

            self.config.theme = theme_name
        except Exception as ex:
            print(f"ERROR ad styler.py:\n{ex}")