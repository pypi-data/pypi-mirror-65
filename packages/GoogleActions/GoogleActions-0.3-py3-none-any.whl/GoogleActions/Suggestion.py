class Suggestion(dict):
    """
    {
      "title": string,
    }
    """

    def __init__(self, title: str):
        super().__init__()

        self['title'] = title
