class Receipt(dict):
    """
    {
      "confirmedActionOrderId": string,
      "userVisibleOrderId": string,
    }
    """

    def __init__(self, user_visible_order_id: str = None, confirmed_action_order_id: str = None):
        super().__init__()

        if user_visible_order_id is not None:
            self['userVisibleOrderId'] = user_visible_order_id

        if confirmed_action_order_id is not None:
            self['confirmedActionOrderId'] = confirmed_action_order_id
