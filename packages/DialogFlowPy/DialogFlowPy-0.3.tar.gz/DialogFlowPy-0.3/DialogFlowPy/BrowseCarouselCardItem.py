from DialogFlowPy import UrlTypeHint
from DialogFlowPy.Image import Image
from DialogFlowPy.OpenUrlAction import OpenUrlAction


class BrowseCarouselCardItem(dict):
    """
    {
      'openUrIAction': {
        object(OpenUrlAction)
      },
      'title': string,
      'description': string,
      'image': {
        object(Image)
      },
      'footer': string
    }
    """

    def __init__(self, open_uri_action: OpenUrlAction, title: str, description: str, image: Image, footer: str):
        super(BrowseCarouselCardItem, self).__init__()

        self['openUriAction'] = open_uri_action
        self['footer'] = footer
        self['image'] = image
        self['title'] = title
        self['description'] = description

    @property
    def open_uri_action(self):
        return self.get('openUriAction')

    @open_uri_action.setter
    def open_uri_action(self, open_uri_action: OpenUrlAction):
        self['openUriAction'] = open_uri_action

    def add_open_uri_action(self, url: str, url_type_hint: UrlTypeHint):
        self.open_uri_action = OpenUrlAction(url=url, url_type_hint=url_type_hint)
        return self.open_uri_action

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title: str):
        self['title'] = title

    @property
    def description(self):
        return self.get('description')

    @description.setter
    def description(self, description):
        self['description'] = description

    @property
    def image(self):
        return self.get('image')

    @image.setter
    def image(self, image: Image):
        self['image'] = image

    def add_image(self, image_uri: str, accessibility_text: str = '') -> Image:
        self['image'] = Image(image_uri=image_uri, accessibility_text=accessibility_text)
        return self['image']

    @property
    def footer(self):
        return self.get('footer')

    @footer.setter
    def footer(self, footer: str):
        self['footer'] = footer
