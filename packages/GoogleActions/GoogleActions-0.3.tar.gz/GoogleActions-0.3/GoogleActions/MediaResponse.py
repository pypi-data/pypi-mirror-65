from typing import List
from . import MediaType
from .MediaObject import MediaObject
from .Image import Image


class MediaResponse(dict):
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

    def __init__(self, media_type: MediaType, media_objects: List[MediaObject]):
        super().__init__()

        self.media_type = media_type
        self['mediaObjects'] = list()

        self.add_media_objects(media_objects)

    @property
    def media_type(self):
        return MediaType(self.get('media_type'))

    @media_type.setter
    def media_type(self, media_type: MediaType):
        self['mediaType'] = media_type.name

    @property
    def media_objects(self):
        return self.get('mediaObjects')

    @media_objects.setter
    def media_objects(self, media_objects_list):
        self['mediaObjects'] = media_objects_list

    def add_media_objects(self, objects: List[MediaObject]) -> List[MediaObject]:
        for item in objects:
            self['mediaObjects'].append(item)

        return self['mediaObjects']

    def add_media_object(self, name: str, description: str = '', content_url: str = '', image_url: str = '',
                         image_text: str = '', image_height: int = 0, image_width: int = 0, icon_url: str = '',
                         icon_text: str = '', icon_height: int = 0, icon_width: int = 0) -> MediaObject:
        media_object = MediaObject(name=name, description=description, content_url=content_url,
                                   large_image=Image(url=image_url, accessibility_text=image_text,
                                                     height=image_height, width=image_width),
                                   icon=Image(url=icon_url,
                                              accessibility_text=icon_text,
                                              height=icon_height,
                                              width=icon_width))
        self['mediaObjects'].append(media_object)
        return media_object
