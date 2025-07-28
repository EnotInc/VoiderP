import json
import os

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.voider")
        self.config_path = os.path.join(self.config_dir, "config.json")

        self.default_config ={
            "files":{
                "LastFile" : "",
                "RootPath" : "",
                "AutoSave" : 1
            },
            "editor": {
                "Theme" : "light",
                "Maximized" : 1,
                "WindowW" : 1000,
                "WindowH" : 600,
                "Font" :{
                    "Family" : "'Consolas', monospace",
                    "Size" : 16
                },
                "RowNumbers" : 0,
                "CursorStyle" : 3,
                "ShowTerminal" : 0,
                "WrapMode" : 0
            },
            "keybindings":{
                "Save" : "Ctrl+S",
                "Save" : "Ctrl+Shift+S",
                "Open" : "Ctrl+O",
            }
        }
        self.config = self.load_config()

        self.root_path = self.config["files"]["RootPath"]
        self.last_file = self.config["files"]["LastFile"]
        self.auto_save = self.config["files"]["AutoSave"]

        self.theme = self.config["editor"]["Theme"]

        self.maximized = self.config["editor"]["Maximized"]
        self.window_w = self.config["editor"]["WindowW"]
        self.window_h = self.config["editor"]["WindowH"]

        self.font_size = self.config["editor"]["Font"]["Size"]
        self.font_family = self.config["editor"]["Font"]["Family"]

        self.wrap_mode = self.config["editor"]["WrapMode"]
        self.row_numbers = self.config["editor"]["RowNumbers"]
        self.cursor_style = self.config["editor"]["CursorStyle"]
        self.show_terminal = self.config["editor"]["ShowTerminal"]
		
    def load_config(self):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                return user_config
        except:
            return self.default_config.copy()

    def save_config(self):
        self.config["files"]["RootPath"] = self.root_path 
        self.config["files"]["LastFile"] = self.last_file
        self.config["files"]["AutoSave"] = self.auto_save

        self.config["editor"]["Theme"] = self.theme
	
        self.config["editor"]["Maximized"] = self.maximized
        self.config["editor"]["WindowW"] = self.window_w
        self.config["editor"]["WindowH"] = self.window_h

        self.config["editor"]["Font"]["Size"] = self.font_size
        self.config["editor"]["Font"]["Family"] = self.font_family

        self.config["editor"]["RowNumbers"] = self.row_numbers
        self.config["editor"]["CursorStyle"] = self.cursor_style
        self.config["editor"]["ShowTerminal"] = self.show_terminal
        self.config["editor"]["WrapMode"] = self.wrap_mode

        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)