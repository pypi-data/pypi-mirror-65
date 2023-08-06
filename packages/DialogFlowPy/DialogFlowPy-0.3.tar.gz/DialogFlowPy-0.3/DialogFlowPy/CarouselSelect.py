from typing import List

from DialogFlowPy.CarouselItem import CarouselItem
from DialogFlowPy.Image import Image
from DialogFlowPy.SelectOptionInfo import SelectOptionInfo


class CarouselSelect(dict):
    """
    {
      'items': [
        {
          object(carouselItem)
        }
      ]
    }
    """

    def __init__(self, carousel_items: List[CarouselItem]):
        super(CarouselSelect, self).__init__()

        self['items'] = []
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['items'].append(item)

    @property
    def carousel_items(self):
        return self.get('items')

    @carousel_items.setter
    def carousel_items(self, carousel_items_list):
        self['items'] = carousel_items_list

    def add_carousel_items(self, carousel_items: CarouselItem) -> List[CarouselItem]:
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self.carousel_items.append(item)
        return self.carousel_items

    def add_carousel_item(self, key: str, title: str, description: str = '', image_uri: str = '', image_text: str = '',
                          synonyms: List[str] = None) -> CarouselItem:
        if synonyms is None:
            synonyms = []

        carousel_item = CarouselItem(title=title, description=description, image=Image(image_uri=image_uri,
                                                                                       accessibility_text=image_text),
                                     option_info=SelectOptionInfo(key, *synonyms))
        self['item_list'].append(carousel_item)
        return carousel_item
