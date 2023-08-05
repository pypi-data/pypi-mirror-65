from typing import List
from .VersionsFilter import VersionsFilter
from . import UrlTypeHint
from .AndroidApp import AndroidApp
from .Image import Image
from .OpenUrlAction import OpenUrlAction


class CarouselBrowseItem(dict):
    """
    {
    "title": string,
    "description": string,
    "footer": string,
    "image": {
    object (Image)
    },
    "openUrlAction": {
    object (OpenUrlAction)
    }
    }
    """

    def __init__(self, title: str = '', description: str = '', footer: str = '', image: Image = None,
                 open_url_action: OpenUrlAction = None):
        super().__init__()

        if open_url_action is not None:
            self['openUrlAction'] = open_url_action

        if image is not None:
            self['image'] = image

        if title is not None:
            self['title'] = title

        if description is not None:
            self['description'] = description

        if footer is not None:
            self['footer'] = footer

    def add_option_info(self, url: str, android_app_package_name: str, android_versions_list: List[int],
                        type_hint: UrlTypeHint) -> OpenUrlAction:
        versions_list = [VersionsFilter(min_version=min(android_versions_list), max_version=max(android_versions_list))]
        self['openUrlAction'] = OpenUrlAction(action_url=url,
                                              android_app=AndroidApp(package_name=android_app_package_name,
                                                                     versions_list=versions_list),
                                              type_hint=type_hint)
        return self['openUrlAction']

    def add_image(self, url: str, accessibility_text: str = '', height: int = 0, width: int = 0) -> Image:
        self['image'] = Image(url=url, accessibility_text=accessibility_text, height=height, width=width)
        return self['image']
