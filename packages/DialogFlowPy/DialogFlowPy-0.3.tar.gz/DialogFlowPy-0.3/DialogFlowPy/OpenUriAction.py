class OpenUriAction(dict):
    """"
        {
      "uri": string
    }
    """

    def __init__(self, uri: str):
        super().__init__()

        self['uri'] = uri

    @property
    def output(self):
        return {
            "uri": self['uri']
        }
