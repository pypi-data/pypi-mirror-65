class Text(dict):
    """
    {
      "text": [
        string
      ]
    }
    """

    def __init__(self, *texts: str):
        super(Text, self).__init__()
        self['text'] = []

        self['text'].extend(texts)
