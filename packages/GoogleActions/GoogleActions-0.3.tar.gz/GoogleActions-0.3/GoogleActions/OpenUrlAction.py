from . import UrlTypeHint
from .AndroidApp import AndroidApp


class OpenUrlAction(dict):
    """
    {
      "url": string,
      "androidApp": {
        object(AndroidApp)
      },
      "urlTypeHint": enum(UrlTypeHint)
    }
    """

    def __init__(self, action_url: str = '', android_app: AndroidApp = None, type_hint: UrlTypeHint = None):
        super().__init__()

        if android_app is not None:
            self['androidApp'] = android_app

        if type_hint is not None:
            self.url_type_hint = type_hint

        if action_url is not None:
            self['url'] = action_url

    def add_android_app(self, package_name: str, versions_list) -> AndroidApp:
        self['androidApp'] = AndroidApp(package_name=package_name, versions_list=versions_list)

        return self['androidApp']

    @property
    def action_url(self):
        return self.get('url')

    @action_url.setter
    def action_url(self, url: str):
        self['url'] = url

    @property
    def url_type_hint(self):
        return UrlTypeHint(self.get('urlTypeHint'))

    @url_type_hint.setter
    def url_type_hint(self, url_type_hint: UrlTypeHint):
        self['urlTypeHint'] = url_type_hint.name
