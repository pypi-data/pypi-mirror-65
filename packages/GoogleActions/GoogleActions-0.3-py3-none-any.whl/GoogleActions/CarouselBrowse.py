from typing import List
from . import ImageDisplayOptions, UrlTypeHint
from .AndroidApp import AndroidApp
from .CarouselBrowseItem import CarouselBrowseItem
from .Image import Image
from .OpenUrlAction import OpenUrlAction


class CarouselBrowse(dict):
    """
    {
      "item_list": [
        {
          object(Item)
        }
      ],
      "imageDisplayOptions": enum(ImageDisplayOptions)
    }
    """

    def __init__(self, image_display_options: ImageDisplayOptions, carousel_browse_items: List[CarouselBrowseItem]):
        super().__init__()

        super(CarouselBrowse, self).__init__()

        self.image_display_options = image_display_options

        self['item_list'] = list()
        self.add_items(carousel_browse_items)

    @property
    def image_display_options(self):
        return ImageDisplayOptions(self.get('imageDisplayOptions'))

    @image_display_options.setter
    def image_display_options(self, image_display_options: ImageDisplayOptions):
        self['imageDisplayOptions'] = image_display_options.name

    def add_items(self, items: List[CarouselBrowseItem]) -> List[CarouselBrowseItem]:
        for item in items:
            assert isinstance(item, CarouselBrowseItem)
            self['item_list'].append(item)

        return self['item_list']

    def add_item(self, title: str = '', description: str = '', footer: str = '', image_url: str = '',
                 accessibility_text: str = '', image_height: int = 0, image_width: int = 0,
                 action_url: str = '', android_app_package_name: str = '', android_versions_list: List[int] = None,
                 type_hint: UrlTypeHint = None) -> CarouselBrowseItem:
        item = CarouselBrowseItem(title=title, description=description,
                                  image=Image(url=image_url, accessibility_text=accessibility_text,
                                              height=image_height, width=image_width), footer=footer,
                                  open_url_action=OpenUrlAction(action_url=action_url,
                                                                android_app=AndroidApp(
                                                                    package_name=android_app_package_name,
                                                                    versions_list=android_versions_list),
                                                                type_hint=type_hint))
        self['item_list'].append(item)
        return item
