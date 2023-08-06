from DialogFlowPy.OpenUriAction import OpenUriAction


class Button(dict):
    """
    {
      "title": string,
      "openUriAction": {
        object(OpenUriAction)
      }
    }
    """

    def __init__(self, title: str = '', open_uri_action: OpenUriAction = None):
        super().__init__()
        if title is not None:
            self['title'] = title

        if open_uri_action is not None:
            self['openUriAction'] = open_uri_action

    def add_open_uri_action(self, uri: str = ''):
        self['openUriAction'] = OpenUriAction(uri=uri)
        return self['openUriAction']

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title: str):
        self['title'] = title

    @property
    def open_uri_action(self):
        return self.get('openUriAction')

    @open_uri_action.setter
    def open_uri_action(self, open_uri_action):
        self['openUriAction'] = open_uri_action
