from typing import List
from .OrderUpdate import OrderUpdate
from .Price import Price
from .Action import Action
from .OrderState import OrderState
from .UserNotification import UserNotification
from .CancellationInfo import CancellationInfo
from .ReturnInfo import ReturnInfo
from .FulfillmentInfo import FulfillmentInfo
from .InTransitInfo import InTransitInfo
from .LineItemUpdate import LineItemUpdate
from .Receipt import Receipt
from .RejectionInfo import RejectionInfo
from .Extension import Extension


class StructuredResponse(dict):
    """
    {
      "orderUpdate": {
        object(OrderUpdate)
      },
    }
    """

    def __init__(self, order_update: OrderUpdate = None):
        super().__init__()

        self['orderUpdate'] = order_update

    def add_order_update(self, google_order_id: str = '', action_order_id: str = '', order_state: OrderState = None,
                         order_management_actions_list: List[Action] = None, receipt: Receipt = None,
                         update_time: str = '',
                         total_price: Price = None, line_item_updates: LineItemUpdate = None,
                         user_notification: UserNotification = None,
                         info_extension: Extension = None, rejection_info: RejectionInfo = None,
                         cancellation_info: CancellationInfo = None,
                         in_transit_info: InTransitInfo = None, fulfillment_info: FulfillmentInfo = None,
                         return_info: ReturnInfo = None) -> OrderUpdate:
        self['orderUpdate'] = OrderUpdate(google_order_id=google_order_id, action_order_id=action_order_id,
                                          order_state=order_state,
                                          order_management_actions_list=order_management_actions_list,
                                          receipt=receipt, update_time=update_time, total_price=total_price,
                                          line_item_updates=line_item_updates, user_notification=user_notification,
                                          info_extension=info_extension, rejection_info=rejection_info,
                                          cancellation_info=cancellation_info, in_transit_info=in_transit_info,
                                          fulfillment_info=fulfillment_info, return_info=return_info)
        return self['orderUpdate']
