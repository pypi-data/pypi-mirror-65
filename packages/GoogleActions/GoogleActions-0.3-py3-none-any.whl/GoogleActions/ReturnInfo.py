class ReturnInfo(dict):
    """
    {
      "reason": string,
    }
    """

    def __init__(self, reason):
        super(ReturnInfo, self).__init__()

        self['reason'] = reason
