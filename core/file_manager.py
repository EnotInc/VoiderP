import os

class FileManager():
    def __init__(self, config, text_buffer):
        self.config = config
        self.buffer = text_buffer
        self.current_file = ""
        self.root_path = ""

    def load_file(self, path):
        try:
            if path != "" and os.path.exists(path):
                if  self.buffer.changed and self.current_file != "":
                    self.save_file()
                with open(path, "r", encoding="utf-8") as f:
                    self.current_file = path 
                    self.config.last_file = path
                    self.buffer.text = f.read()

        except Exception as e:
            print(e)

    def save_file(self):
        try:
            if self.current_file != "":
                _path = self.current_file
                with open(_path, "w", encoding="utf-8") as f:
                    f.write(self.buffer.text)
                self.buffer.changed = False
                
        except Exception as e:
            print(e, _path)

    def save_as_file(self, path):
        try:
            _path = path
            with open(_path, "w", encoding="utf-8") as f:
                f.write(self.buffer.text)
            self.buffer.changed = False

        except Exception as e:
            print(e)
    
    def purge_editor(self):
        self.save_file()
        self.buffer.text = ""
        self.current_file = ""
        self.config.last_file = ""
    
    def open_folder(self, path):
        self.root_path = path
        self.config.root_path = path

    def create_new_dirrectory():
        pass

    def remane_item():
        pass

    def remove_item():
        pass