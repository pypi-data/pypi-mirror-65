class EventInput(dict):
    """
    {
      "name": string,
      "parameters": {
        object
      },
      "languageCode": string
    }
    """

    def __init__(self, name: str, language_code: str, **parameters):
        super().__init__()

        self['name'] = name
        self['languageCode'] = language_code
        self['parameters'] = parameters

    def add_parameters(self, **kwargs) -> dict:
        self['parameters'].update(kwargs)
        return self['parameters']
