class FileManager():
    def __init__(self, text_buffer):
        self.buffer = text_buffer
        # тут будет подгрузка корневого файла
        pass

    def load_file(self, path):
        with open(path, "r") as f:
            self.buffer.text = f.read()

    def save_file(self, path):
        path = path
        with open(path, "w") as f:
            f.write(self.buffer.text)

    def create_new_file():
        pass

    def create_new_dirrectory():
        pass

    def remane_item():
        pass

    def remove_item():
        pass