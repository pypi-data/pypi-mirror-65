class UserNotification(dict):
    """
    {
      "title": string,
      "text": string,
    }
    """

    def __init__(self, text: str = '', title: str = ''):
        super().__init__()

        self['text'] = text
        self['title'] = title
