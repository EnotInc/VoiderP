def apply_theme(theme_name):
    try:
        theme_file = f"sources/styles/{theme_name}.qss"
        with open(theme_file, "r") as t:
            _style = t.read()

        return _style
    except Exception as ex:
        print(ex)
        return None