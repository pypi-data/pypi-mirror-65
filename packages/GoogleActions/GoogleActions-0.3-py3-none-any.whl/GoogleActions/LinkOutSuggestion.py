class LinkOutSuggestion(dict):
    """
    {
      "destinationName": string,
      "url": string,
    }
    """

    def __init__(self, url: str = '', destination_name: str = ''):
        super().__init__()

        self['url'] = url
        self['destinationName'] = destination_name
