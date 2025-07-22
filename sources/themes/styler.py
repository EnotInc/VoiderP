import json

class Styler:
    def __init__(self, config):
        self.font_size = config.config["editor"]["Font"]["Size"]
        self.font_family = config.config["editor"]["Font"]["Family"]
        self.theme = config.config["editor"]["Theme"]

    def apply_theme(self, theme_name):
        try:
            theme_file = "sources/themes/style.qss"
            with open(theme_file, "r") as s:
                _style = s.read()
            
            with open("sources/themes/colors.json") as t:
                themes = json.load(t)[theme_name]

            for var, value in themes.items():
                _style = _style.replace(var, value)

            self.theme = theme_name
            _style = _style.replace("@font_size", f"{self.font_size}px")
            _style = _style.replace("@font_family", self.font_family)

            return _style
        except Exception as ex:
            print(ex)
            return None