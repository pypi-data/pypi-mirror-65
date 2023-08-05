class OrderState(dict):
    """
    {
      "state": string,
      "label": string,
    }
    """

    def __init__(self, state: str = None, label: str = None):
        super().__init__()

        if state is not None:
            self['state'] = state
        if label is not None:
            self['label'] = label
