import json

def apply_theme(theme_name):
    try:
        theme_file = f"sources/themes/style.qss"
        with open(theme_file, "r") as s:
            _style = s.read()
        
        with open(f"sources/themes/colors.json") as t:
            themes = json.load(t)[theme_name]

        for var, value in themes.items():
            _style = _style.replace(var, value)

        return _style
    except Exception as ex:
        print(ex)
        return None