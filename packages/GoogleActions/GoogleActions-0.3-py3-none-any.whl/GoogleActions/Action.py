from . import ActionType
from .Button import Button
from .OpenUrlAction import OpenUrlAction


class Action(dict):
    """
    {
      "type": enum(ActionType),
      "button": {
        object(Button)
      },
    }
    type
    enum(ActionType)
    Type of action.

    button
    object(Button)
    Button label and link.
    """

    def __init__(self, button: Button = None, action_type: ActionType = None):
        super().__init__()
        if button is None:
            button = dict()
        self.button = button

        self.action_type = action_type

    @property
    def button(self):
        return self.get('button')

    @button.setter
    def button(self, button: Button):
        self['button'] = button

    @property
    def action_type(self):
        return ActionType(self.get('type'))

    @action_type.setter
    def action_type(self, action_type: ActionType):
        self['type'] = action_type.name

    def add_button(self, title: str, url: str = '') -> Button:
        assert isinstance(title, str)
        assert isinstance(url, str)

        self['button'] = Button(title=title, open_url_action=OpenUrlAction(action_url=url))

        return self['button']
