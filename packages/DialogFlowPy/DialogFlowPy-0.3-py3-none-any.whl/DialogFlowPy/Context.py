class Context(dict):
    """
    {
      "name": string,
      "lifespanCount": number,
      "parameters": {
        object
      }
    }
    """

    def __init__(self, name: str, lifespan_count: int = 0, **parameters):
        super().__init__()

        self['name'] = name
        self['lifespanCount'] = lifespan_count
        self['parameters'] = parameters

    def add_parameters(self, **parameters) -> dict:
        self['parameters'].update(**parameters)
        return self['parameters']

    def update_parameters(self, **parameters) -> dict:
        self['parameters'].update(**parameters)
        return self['parameters']

    @property
    def name(self):
        return self['name']

    @name.setter
    def name(self, value):
        self['name'] = value
