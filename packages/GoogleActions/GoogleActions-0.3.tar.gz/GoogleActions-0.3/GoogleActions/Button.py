from .OpenUrlAction import OpenUrlAction
from .AndroidApp import AndroidApp
from . import UrlTypeHint
from .VersionsFilter import VersionsFilter


class Button(dict):
    """
    {
      "title": string,
      "openUrlAction": {
        object(OpenUrlAction)
      },
    }
    """

    def __init__(self, title: str = '', open_url_action: OpenUrlAction = None):
        super(Button, self).__init__()

        if title is not None:
            self['title'] = title
        if open_url_action is not None:
            self['openUrlAction'] = open_url_action

    def add_open_url_action(self, url: str = '', package_name: str = '', type_hint: UrlTypeHint = None,
                            versions_list: VersionsFilter = None):

        self['openUrlAction'] = OpenUrlAction(action_url=url,
                                              android_app=AndroidApp(package_name=package_name,
                                                                     versions_list=versions_list),
                                              type_hint=type_hint)

        return self['openUrlAction']
