from typing import List

from DialogFlowPy.Image import Image
from DialogFlowPy.SelectOptionInfo import SelectOptionInfo


class CarouselItem(dict):
    """
    {
      'info': {
        object(SelectItemInfo)
      },
      'title': string,
      'description': string,
      'image': {
        object(Image)
      }
    }
    """

    def __init__(self, title: str, description: str, image: Image = None, option_info: SelectOptionInfo = None):
        super(CarouselItem, self).__init__()

        if option_info is not None:
            self['info'] = option_info

        if image is not None:
            self['image'] = image

        if title is not None:
            self['title'] = title

        if description is not None:
            self['description'] = description

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
    def select_option_info(self):
        return self.get('info')

    @select_option_info.setter
    def select_option_info(self, select_option_info: SelectOptionInfo):
        self['info'] = select_option_info

    def add_option_info(self, key: str, synonyms: List[str]) -> SelectOptionInfo:
        self['info'] = SelectOptionInfo(key=key, synonyms=synonyms)
        return self['info']
