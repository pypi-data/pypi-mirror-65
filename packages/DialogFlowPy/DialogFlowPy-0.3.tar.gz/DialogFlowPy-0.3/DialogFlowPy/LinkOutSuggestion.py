class LinkOutSuggestion(dict):
    """
    {
      "destinationName": string,
      "url": string,
    }
    """

    def __init__(self, uri: str = '', destination_name: str = ''):
        super().__init__()

        self['uri'] = uri
        self['destinationName'] = destination_name
