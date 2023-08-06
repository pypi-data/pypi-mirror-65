from typing import List

from DialogFlowPy.Image import Image
from DialogFlowPy.ListItem import ListItem
from DialogFlowPy.SelectOptionInfo import SelectOptionInfo


class ListSelect(dict):
    """
    {
      'title': string,
      'subtitle': string
      'items': [
        {
          object(ListItem)
        }
      ]
    }


    """

    def __init__(self, title: str, subtitle: str, list_items: List[ListItem]):
        super().__init__()

        self.list_items = []

        for item in list_items:
            assert isinstance(item, ListItem)
            self.list_items.append(item)

        self.title = title
        self.subtitle = subtitle

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title: str):
        self['title'] = title

    @property
    def subtitle(self):
        return self.get('subtitle')

    @subtitle.setter
    def subtitle(self, subtitle: str):
        self['subtitle'] = subtitle

    @property
    def list_items(self):
        return self.get('items')

    @list_items.setter
    def list_items(self, items_list):
        self['items'] = items_list

    def add_list_items(self, list_items: ListItem) -> List[ListItem]:
        for item in list_items:
            assert isinstance(item, ListItem)
            self.list_items.append(item)
        return self.list_items

    def add_list_item(self, key: str, title: str, description: str = '', image_uri: str = '',
                      accessibility_text: str = '', synonyms: List[str] = None) -> bool:
        if synonyms is None:
            synonyms = []

        self.list_items.append(ListItem(title=title, description=description, image=Image(
            image_uri=image_uri, accessibility_text=accessibility_text),
                                        option_info=SelectOptionInfo(key=key, synonyms=synonyms)))
        return True
