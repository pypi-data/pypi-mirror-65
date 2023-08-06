from DialogFlowPy import UrlTypeHint


class OpenUrlAction(dict):
    """"
        {
      "url": string,
      "urlTypeHint": Object(UrlTypeHint)
    }
    """

    def __init__(self, url: str, url_type_hint: UrlTypeHint):
        super().__init__()

        self.url = url
        self.url_type_hint = url_type_hint

    @property
    def url(self):
        return self.get('url')

    @url.setter
    def url(self, url: str):
        self['url'] = url

    @property
    def url_type_hint(self):
        return UrlTypeHint(self.get('urlTypeHint'))

    @url_type_hint.setter
    def url_type_hint(self, url_type_hint: UrlTypeHint):
        self['urlTypeHint'] = url_type_hint.name
