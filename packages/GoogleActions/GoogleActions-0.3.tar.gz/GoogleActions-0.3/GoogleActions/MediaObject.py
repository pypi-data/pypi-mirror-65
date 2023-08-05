from .Image import Image


class MediaObject(dict):
    """
    {
      "name": string,
      "description": string,
      "contentUrl": string,

      // Union field image can be only one of the following:
      "largeImage": {
        object(Image)
      },
      "icon": {
        object(Image)
      }
      // End of list of possible types for union field image.
    }
    """

    def __init__(self, name: str, description: str = '', content_url: str = '',
                 large_image: Image = None,
                 icon: Image = None):
        super().__init__()

        self['name'] = name
        if description is not None:
            self['description'] = description
        if content_url is not None:
            self['contentUrl'] = content_url

        if large_image is not None:
            self['largeImage'] = large_image

        if icon is not None:
            self['icon'] = icon

    def add_large_image(self, url: str, text: str = '', height: int = 0, width: int = 0) -> Image:
        self['largeImage'] = Image(url=url, accessibility_text=text, height=height, width=width)

        return self['largeImage']

    def add_icon(self, url: str, text: str = '', height: int = 0, width: int = 0) -> Image:
        self['icon'] = Image(url=url, accessibility_text=text, height=height, width=width)

        return self['icon']
