from DialogFlowPy.Image import Image
from DialogFlowPy.SelectOptionInfo import SelectOptionInfo


class ListItem(dict):
    """
    {
      'info': {
        object(OptionInfo)
      },
      'title': string,
      'description': string,
      'image': {
        object(Image)
      }
    }
    """

    def __init__(self, title: str, description: str, image: Image, option_info: SelectOptionInfo):
        super().__init__()

        self.option_info = option_info
        self.image = image
        self.title = title
        self.description = description

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
    def description(self, description: str):
        self['description'] = description

    @property
    def option_info(self):
        return self.get('info')

    @option_info.setter
    def option_info(self, option_info: str):
        self['info'] = option_info

    @property
    def image(self):
        return self.get('image')

    @image.setter
    def image(self, image: Image):
        self['image'] = image

    def add_image(self, image_uri: str, accessibility_text: str = '') -> Image:
        self['image'] = Image(image_uri=image_uri, accessibility_text=accessibility_text)
        return self['image']
