class FileManager():
    def __init__(self, text_buffer):
        self.buffer = text_buffer

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.buffer.text = f.read()
                if self.buffer.changed:
                    print("file was changed but not saves")

        except Exception as e:
            print(e)

    def save_file(self, path):
        try:
            path = path
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.buffer.text)
        except Exception as e:
            print(e)
    
    def create_new_dirrectory():
        pass

    def remane_item():
        pass

    def remove_item():
        pass