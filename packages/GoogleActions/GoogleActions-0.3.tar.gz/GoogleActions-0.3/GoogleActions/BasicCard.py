from . import ImageDisplayOptions
from .Button import Button
from .Image import Image
from .OpenUrlAction import OpenUrlAction
from typing import List


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
      "imageDisplayOptions": enum(ImageDisplayOptions),
    }
    """

    def __init__(self, title: str = '', formatted_text: str = '', subtitle: str = '', image: Image = None,
                 image_display_options: ImageDisplayOptions = None, buttons: List[Button] = None):

        super(BasicCard, self).__init__()
        if buttons is None:
            buttons = list()

        self['buttons'] = list()

        for item in buttons:
            print('item: ', type(item), item)
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

        if image_display_options is not None:
            self['image_display_options'] = image_display_options

    def add_button(self, title: str, url: str) -> Button:
        button = Button(title=title, open_url_action=OpenUrlAction(action_url=url))
        self['buttons'].append(button)

        return button
