from .OptionInfo import OptionInfo
from .Image import Image
from typing import List


class CarouselItem(dict):
    """
    {
      'optionInfo': {
        object(OptionInfo)
      },
      'title': string,
      'description': string,
      'image': {
        object(Image)
      }
    }
    """

    def __init__(self, title: str = '', description: str = '', image: Image = None, option_info: OptionInfo = None):
        super(CarouselItem, self).__init__()

        if option_info is not None:
            self['optionInfo'] = option_info

        if image is not None:
            self['image'] = image

        if title is not None:
            self['title'] = title

        if description is not None:
            self['description'] = description

    def add_option_info(self, key: str, synonyms: List[str]) -> OptionInfo:
        self['optionInfo'] = OptionInfo(key=key, synonyms=synonyms)
        return self['optionInfo']

    def add_image(self, url: str, accessibility_text: str = '', height: int = 0, width: int = 0) -> Image:
        self['image'] = Image(url=url, accessibility_text=accessibility_text, height=height, width=width)
        return self['image']
