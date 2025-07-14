class TextBuffer:
    def __init__(self):
        self._text = ""
        self.ischanged = False
        
    @property
    def text(self):
        self.ischanged = False
        return self._text
    
    @text.setter
    def text(self, value):
        self.ischanged = True
        self._text = value


    @property
    def isChanged(self):
        return self.isChanged

    @isChanged.setter
    def isChanged(self, value: bool):
        self.isChanged = value
    
