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
                "AutoSave" : ""
            },
            "editor": {
                "Theme" : "light",
                "Maximized" : 1,
                "WindowH" : 1000,
                "WindowV" : 600,
                "Font" :{
                    "Family" : "'Consolas', monospace",
                    "Size" : 16
                },
                "RowNumbers" : 0,
                "RelativeNumbers" : 0,
                "SintaxHightlight": 0,
                "CursorStyle" : 1,
            },
            "keybindings":{
                "Save" : "Ctrl+S",
                "Save" : "Ctrl+Shift+S",
                "Open" : "Ctrl+O",
            }
        }
        self.config = self.load_config()

    def load_config(self):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                return user_config
        except:
            return self.default_config.copy()

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)