from typing import List
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
from .Button import Button
from .OpenUrlAction import OpenUrlAction
from .AndroidApp import AndroidApp
from . import ActionType, PriceType, ReasonType
from .Money import Money


class OrderUpdate(dict):
    """
    {
      "googleOrderId": string,
      "actionOrderId": string,
      "orderState": {
        object(OrderState)
      },
      "orderManagementActions": [
        {
          object(Action)
        }
      ],
      "receipt": {
        object(Receipt)
      },
      "updateTime": string,
      "totalPrice": {
        object(Price)
      },
      "lineItemUpdates": {
        string: {
          object(LineItemUpdate)
        },
        ...
      },
      "userNotification": {
        object(UserNotification)
      },
      "infoExtension": {
        "@type": string,
        field1: ...,
        ...
      },

      // Union field info can be only one of the following:
      "rejectionInfo": {
        object(RejectionInfo)
      },
      "cancellationInfo": {
        object(CancellationInfo)
      },
      "inTransitInfo": {
        object(InTransitInfo)
      },
      "fulfillmentInfo": {
        object(FulfillmentInfo)
      },
      "returnInfo": {
        object(ReturnInfo)
      },
      // End of list of possible types for union field info.
    }
    """

    def __init__(self, google_order_id: str = '', action_order_id: str = '', order_state: OrderState = None,
                 order_management_actions_list: List[Action] = None, receipt: Receipt = None, update_time: str = '',
                 total_price: Price = None, line_item_updates: LineItemUpdate = None,
                 user_notification: UserNotification = None,
                 info_extension: Extension = None, rejection_info: RejectionInfo = None,
                 cancellation_info: CancellationInfo = None,
                 in_transit_info: InTransitInfo = None, fulfillment_info: FulfillmentInfo = None,
                 return_info: ReturnInfo = None):
        super(OrderUpdate, self).__init__()

        if receipt is not None:
            self['receipt'] = receipt
        if info_extension is not None:
            self['infoExtension'] = info_extension
        if return_info is not None:
            self['returnInfo'] = return_info
        if user_notification is not None:
            self['userNotification'] = user_notification
        if rejection_info is not None:
            self['rejectionInfo'] = rejection_info
        if update_time is not None:
            self['updateTime'] = update_time
        if line_item_updates is not None:
            self['lineItemUpdates'] = line_item_updates
        if fulfillment_info is not None:
            self['fulfillmentInfo'] = fulfillment_info
        if total_price is not None:
            self['totalPrice'] = total_price
        if in_transit_info is not None:
            self['inTransitInfo'] = in_transit_info
        if action_order_id is not None:
            self['actionOrderId'] = action_order_id
        if cancellation_info is not None:
            self['cancellationInfo'] = cancellation_info
        if order_state is not None:
            self['orderState'] = order_state
        if google_order_id is not None:
            self['googleOrderId'] = google_order_id
        if order_management_actions_list is not None:
            self['orderManagementActions'] = order_management_actions_list
        if rejection_info is not None:
            self['rejectionInfo'] = rejection_info

    def add_order_management_actions(self, order_management_actions) -> List[Action]:
        for item in order_management_actions:
            assert isinstance(item, Action)
            self['orderManagementActions'].append(item)
        return self['orderManagementActions']

    def add_order_management_action(self, title: str, url: str, action_type: ActionType,
                                    android_package_name: str = '', android_versions=None) -> Action:
        if android_versions is None:
            android_versions = []

        if android_package_name is not None:
            android_app = AndroidApp(package_name=android_package_name, versions_list=android_versions)
        else:
            android_app = None

        action: Action = Action(
            button=Button(title=title, open_url_action=OpenUrlAction(action_url=url, android_app=android_app)),
            action_type=action_type)
        self['orderManagementActions'].append(action)
        return action

    def add_receipt(self, user_visible_order_id: str = '', confirmed_action_order_id: str = '') -> Receipt:
        self['receipt'] = Receipt(user_visible_order_id=user_visible_order_id,
                                  confirmed_action_order_id=confirmed_action_order_id)
        return self['receipt']

    def add_total_price(self, price_type: PriceType, amount, currency_code) -> Price:
        self['totalPrice'] = Price(price_type=price_type, amount=Money(amount=amount,
                                                                       currency_code=currency_code))

        return self['totalPrice']

    def add_line_item_updates(self, reason: str, price_type: PriceType, amount: float, currency_code: str,
                              state: str, label: str, extension_type: str, **extension_kwargs) -> LineItemUpdate:
        self['lineItemUpdates'] = LineItemUpdate(reason=reason, price=Price(price_type=price_type,
                                                                            amount=Money(
                                                                                amount=amount,
                                                                                currency_code=currency_code
                                                                            )),
                                                 order_state=OrderState(state=state, label=label),
                                                 extension=Extension(extension_type=extension_type,
                                                                     **extension_kwargs))
        return self['lineItemUpdates']

    def add_user_notification(self, text: str, title: str) -> UserNotification:
        self['userNotification'] = UserNotification(text=text, title=title)
        return self['userNotification']

    def add_info_extension(self, extension_type: str, **kwargs) -> Extension:
        self['infoExtension'] = Extension(extension_type, **kwargs)
        return self['infoExtension']

    def add_rejection_info(self, rejection_type: ReasonType, reason: str) -> RejectionInfo:
        self['rejectionInfo'] = RejectionInfo(rejection_type, reason=reason)
        return self['rejectionInfo']

    def add_cancellation_info(self, reason: str) -> CancellationInfo:
        self['cancellationInfo'] = CancellationInfo(reason=reason)
        return self['cancellationInfo']

    def add_in_transit_info(self, updated_time: str) -> InTransitInfo:
        self['inTransitInfo'] = InTransitInfo(updated_time=updated_time)
        return self['inTransitInfo']

    def add_fulfillment_info(self, delivery_time: str) -> FulfillmentInfo:
        self['fulfillmentInfo'] = FulfillmentInfo(delivery_time=delivery_time)
        return self['fulfillmentInfo']

    def add_return_info(self, reason: str) -> ReturnInfo:
        self['returnInfo'] = ReturnInfo(reason=reason)
        return self['returnInfo']
