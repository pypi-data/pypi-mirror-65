class TableCardCell(dict):
    """
    {
      "text": string
    }
    """

    def __init__(self, text):
        super().__init__()
        self.text = text

    @property
    def text(self):
        return self.get('text')

    @text.setter
    def text(self, text):
        self['text'] = text
