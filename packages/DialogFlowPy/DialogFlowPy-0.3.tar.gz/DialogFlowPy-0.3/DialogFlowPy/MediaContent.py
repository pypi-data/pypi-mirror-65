from typing import List

from DialogFlowPy import ResponseMediaType

from DialogFlowPy.Image import Image
from DialogFlowPy.MediaObject import MediaObject


class MediaContent(dict):
    """
    {
      "mediaType": enum(MediaType),
      "mediaObjects": [
        {
          object(MediaObject)
        }
      ]
    }
    """

    def __init__(self, media_type: ResponseMediaType, media_objects: List[MediaObject]):
        super().__init__()

        self.media_objects = media_objects
        self.media_type = media_type

    @property
    def media_type(self):
        return ResponseMediaType(self.get('media_type'))

    @media_type.setter
    def media_type(self, media_type: ResponseMediaType):
        self['mediaType'] = media_type.name

    @property
    def media_objects(self):
        return self.get('mediaObjects')

    @media_objects.setter
    def media_objects(self, media_objects_list):
        self['mediaObjects'] = media_objects_list

    def add_media_objects(self, objects: MediaObject) -> List[MediaObject]:
        for item in objects:
            self['mediaObjects'].append(item)

        return self['mediaObjects']

    def add_media_object(self, name: str, description: str = '', content_url: str = '', image_uri: str = '',
                         image_text: str = '', icon_uri: str = '', icon_text: str = '') -> MediaObject:
        media_object = MediaObject(name=name, description=description, content_url=content_url,
                                   large_image=Image(image_uri=image_uri, accessibility_text=image_text),
                                   icon=Image(image_uri=icon_uri,
                                              accessibility_text=icon_text))
        self['mediaObjects'].append(media_object)
        return media_object
