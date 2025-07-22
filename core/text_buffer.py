class TextBuffer:
    def __init__(self):
        self._text = ""
        self._changed = False
        
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, value):
        self._changed = value