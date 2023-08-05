class InTransitInfo(dict):
    """
    {
      "updatedTime": string,
    }
    """

    def __init__(self, updated_time: str = None):
        super().__init__()

        if updated_time is not None:
            self['updated_time'] = updated_time
