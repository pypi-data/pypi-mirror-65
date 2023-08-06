from typing import List
from DialogFlowPy.Button import Button
from DialogFlowPy.OpenUriAction import OpenUriAction


class Card(dict):
    """
    {
      "title": string,
      "subtitle": string,
      "imageUri": string,
      "buttons": [
        {
          object(Button)
        }
      ],
    }
    """

    def __init__(self, title: str = '', image_uri: str = '', subtitle: str = '', buttons: List[Button] = None):
        super().__init__()

        self['buttons'] = []

        for item in buttons:
            print(type(item))
            assert isinstance(item, Button)
            self['buttons'].append(item)

        if title is not None:
            self['title'] = title

        if image_uri is not None:
            self['imageUri'] = image_uri

        if subtitle is not None:
            self['subtitle'] = subtitle

    def add_button(self, title: str, uri: str) -> Button:
        button = Button(title=title, open_uri_action=OpenUriAction(uri=uri))
        self['buttons'].append(button)

        return button
