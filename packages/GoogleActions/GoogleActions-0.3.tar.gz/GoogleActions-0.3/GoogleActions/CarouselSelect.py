from typing import List
from .CarouselItem import CarouselItem
from .Image import Image
from .OptionInfo import OptionInfo
from . import ImageDisplayOptions


class CarouselSelect(dict):
    """    
    {
      "title": string,
      "subtitle": string,
      "items": [
        {
          object (CarouselItem)
        }
      ],
      "imageDisplayOptions": enum (ImageDisplayOptions)
    }
    """

    def __init__(self, title: str, subtitle: str, image_display_options: ImageDisplayOptions,
                 carousel_items: CarouselItem):
        super(CarouselSelect, self).__init__()

        self['title'] = title
        self['subtitles'] = subtitle
        self['items'] = []
        self.add_carousel_items(carousel_items)

        self.image_display_options = image_display_options

    @property
    def image_display_options(self):
        return ImageDisplayOptions(self.get('imageDisplayOptions'))

    @image_display_options.setter
    def image_display_options(self, image_display_options: ImageDisplayOptions):
        self['imageDisplayOptions'] = image_display_options.name

    def add_carousel_items(self, carousel_items: CarouselItem) -> List[CarouselItem]:
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['items'].append(item)
        return self['items']

    def add_carousel_item(self, key: str, title: str, description: str = '', image_url: str = '',
                          image_text: str = '',
                          image_height: int = 0, image_width: int = 0, synonyms: List[str] = None) -> CarouselItem:
        carousel_item = CarouselItem(title=title, description=description, image=Image(url=image_url,
                                                                                       accessibility_text=image_text,
                                                                                       height=image_height,
                                                                                       width=image_width),
                                     option_info=OptionInfo(key=key, synonyms=synonyms))
        self['items'].append(carousel_item)
        return carousel_item
