from typing import List
from .Target import Target
from .OrderUpdate import OrderUpdate
from .OrderState import OrderState
from .Action import Action
from .Receipt import Receipt
from .Price import Price
from .LineItemUpdate import LineItemUpdate
from .UserNotification import UserNotification
from .RejectionInfo import RejectionInfo
from .CancellationInfo import CancellationInfo
from .InTransitInfo import InTransitInfo
from .FulfillmentInfo import FulfillmentInfo
from .ReturnInfo import ReturnInfo
from .Extension import Extension
from .Argument import Argument
from .Status import Status
from .Location import Location


class CustomPushMessage(dict):
    """
    {
      "target": {
        object(Target)
      },

      // Union field content can be only one of the following:
      "orderUpdate": {
        object(OrderUpdate)
      },
      "userNotification": {
        object(UserNotification)
      },
      // End of list of possible types for union field content.
    }
    """

    def __init__(self, order_update: OrderUpdate = None, user_notification: UserNotification = None,
                 target: Target = None):
        super(CustomPushMessage, self).__init__()

        if order_update is not None:
            self['orderUpdate'] = order_update

        if user_notification is not None:
            self['userNotification'] = user_notification

        if target is not None:
            self['target'] = target

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

    def add_user_notification(self, text: str, title: str) -> UserNotification:
        self['userNotification'] = UserNotification(text=text, title=title)
        return self['userNotification']

    def add_target(self, intent=None, user_id=None, name: str = '', raw_text: str = '',
                   text_value: str = '', status: Status = None, int_value: str = '', float_value: str = '',
                   bool_value: bool = False, datetime_value: str = '', place_value: Location = None,
                   extension: Extension = None,
                   **structure_values):

        self['target'] = Target(intent=intent, argument=Argument(name=name, raw_text=raw_text,
                                                                 text_value=text_value, status=status,
                                                                 int_value=int_value,
                                                                 float_value=float_value, bool_value=bool_value,
                                                                 datetime_value=datetime_value,
                                                                 place_value=place_value, extension=extension,
                                                                 **structure_values),
                                user_id=user_id)
