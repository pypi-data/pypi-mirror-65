from typing import List
from DialogFlowPy import ImageDisplayOptions
from DialogFlowPy.BrowseCarouselCardItem import BrowseCarouselCardItem
from DialogFlowPy.Image import Image
from DialogFlowPy.OpenUrlAction import OpenUrlAction


class BrowseCarouselCard(dict):
    """
    {
      "items": [
        {
          object(BrowseCarouselCardItem)
        }
      ],
      "imageDisplayOptions": enum(ImageDisplayOptions)
    }
    """

    def __init__(self, image_display_options: ImageDisplayOptions,
                 browse_carousel_card_items: List[BrowseCarouselCardItem]):
        super().__init__()

        super(BrowseCarouselCard, self).__init__()

        self.image_display_options = image_display_options
        self['items'] = []

        self.add_browse_carousel_card_items(browse_carousel_card_items)

    @property
    def image_display_options(self):
        return ImageDisplayOptions(self.get('imageDisplayOptions'))

    @image_display_options.setter
    def image_display_options(self, image_display_options: ImageDisplayOptions):
        self['imageDisplayOptions'] = image_display_options.name

    @property
    def browse_carouse_card_items(self):
        return self.get('items')

    @browse_carouse_card_items.setter
    def browse_carouse_card_items(self, browse_carousel_card_items_list):
        self['items'] = browse_carousel_card_items_list

    def add_browse_carousel_card_items(self, browse_carousel_card_items: List[BrowseCarouselCardItem]):
        for item in browse_carousel_card_items:
            assert isinstance(item, BrowseCarouselCardItem)
            self.browse_carouse_card_items.append(item)

        return self.browse_carouse_card_items

    def add_item(self, open_uri_action: OpenUrlAction, title: str, description: str, image_url: str, image_text: str,
                 footer: str) -> BrowseCarouselCardItem:
        item = BrowseCarouselCardItem(open_uri_action=open_uri_action, title=title, description=description,
                                      image=Image(image_uri=image_url, accessibility_text=image_text), footer=footer)
        self.browse_carouse_card_items.append(item)
        return item
