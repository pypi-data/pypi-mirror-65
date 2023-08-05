class FulfillmentInfo(dict):
    """
    {
      "deliveryTime": string,
    }
    """

    def __init__(self, delivery_time: str = ''):
        super().__init__()

        if delivery_time is not None:
            self['deliveryTime'] = delivery_time
