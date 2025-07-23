import json

class Styler:
    def __init__(self, config):
        self.config = config

    def apply_theme(self, theme_name):
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

            self.config.theme = theme_name

            return _style
        except Exception as ex:
            print(ex)
            return None