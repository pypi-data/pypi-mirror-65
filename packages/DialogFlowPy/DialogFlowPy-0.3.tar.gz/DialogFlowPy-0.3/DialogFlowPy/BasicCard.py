from typing import List

from DialogFlowPy.Button import Button
from DialogFlowPy.Image import Image
from DialogFlowPy.OpenUriAction import OpenUriAction


class BasicCard(dict):
    """
    {
      "title": string,
      "subtitle": string,
      "formattedText": string,
      "image": {
        object(Image)
      },
      "buttons": [
        {
          object(Button)
        }
      ],
    }
    """

    def __init__(self, title: str = '', formatted_text: str = '', subtitle: str = '', image: Image = None,
                 buttons: List[Button] = None):

        super(BasicCard, self).__init__()

        self['buttons'] = []

        for item in buttons:
            assert isinstance(item, Button)
            self['buttons'].append(item)

        if title is not None:
            self['title'] = title

        if formatted_text is not None:
            self['formattedText'] = formatted_text

        if subtitle is not None:
            self['subtitle'] = subtitle

        if image is not None:
            self['image'] = image

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
    def formatted_text(self):
        return self.get('formattedText')

    @formatted_text.setter
    def formatted_text(self, formatted_text: str):
        self['formattedText'] = formatted_text

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
    def buttons(self):
        return self.get('buttons')

    @buttons.setter
    def buttons(self, buttons_list):
        self['buttons'] = buttons_list

    def add_button(self, title: str, uri: str) -> Button:
        button = Button(title=title, open_uri_action=OpenUriAction(uri=uri))
        self.buttons.append(button)

        return button
