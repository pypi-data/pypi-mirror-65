from typing import List
from .RichResponse import RichResponse
from .Item import Item
from .Suggestion import Suggestion
from .LinkOutSuggestion import LinkOutSuggestion
from . import ImageDisplayOptions, MediaType
from .MediaObject import MediaObject
from .ExpectedIntent import ExpectedIntent
from .Extension import Extension
from .Button import Button


class Google(dict):
    """Google data component to be added to DialogFlowOutput
    {
        'expectUserResponse': boolean,
        'userStorage': string
        'richResponse': GoogleRichResponse,
        'systemIntent': GoogleExpectedIntent,
    }

    """

    def __init__(self, expect_user_response: bool = True, rich_response: RichResponse = None, user_storage: str = '',
                 system_intent: ExpectedIntent = None):
        super().__init__()

        if expect_user_response is not None:
            self['expectUserResponse'] = expect_user_response
        if rich_response is not None:
            self['richResponse'] = rich_response
        if system_intent is not None:
            self['systemIntent'] = system_intent
        if user_storage is not None:
            self['userStorage'] = user_storage

    def add_rich_response(self, items_list: List[Item] = None, suggestions: List[Suggestion] = None,
                          link_name: str = '',
                          link_url: str = '') -> RichResponse:

        self['richResponse'] = RichResponse(item_list=items_list, suggestions=suggestions,
                                            link_out_suggestion=LinkOutSuggestion(url=link_url,
                                                                                  destination_name=link_name))
        return self['richResponse']

    def add_system_intent(self, intent: str = '', parameter_name: str = '', input_value: Extension = None) \
            -> ExpectedIntent:

        self['systemIntent'] = ExpectedIntent(intent=intent, parameter_name=parameter_name, input_value=input_value)
        return self['systemIntent']

    def add_items(self, items) -> RichResponse:
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_items(items)
        return self['richResponse']

    def add_simple_response(self, text_to_speech: str, ssml: str, display_text: str) -> RichResponse:
        print('richResponse', self['richResponse'])
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_simple_response(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text)

        return self['richResponse']

    def add_basic_card(self, title: str, formatted_text: str, subtitle: str, image_url: str,
                       image_text: str, image_height: int, image_width: int,
                       image_display_options: ImageDisplayOptions, buttons: Button) -> RichResponse:

        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_basic_card(title=title, formatted_text=formatted_text, subtitle=subtitle,
                                            image_url=image_url, image_text=image_text, image_height=image_height,
                                            image_width=image_width, image_display_options=image_display_options,
                                            buttons)

        return self['richResponse']

    def add_structured_response(self, receipt=None, info_extension=None,
                                return_info=None,
                                user_notification=None, rejection_info=None, update_time=None,
                                line_item_updates=None, fulfillment_info=None,
                                total_price=None,
                                in_transit_info=None, action_order_id=None,
                                cancellation_info=None,
                                order_state=None, google_order_id=None,
                                order_management_actions_list=None) -> RichResponse:
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_structured_response(receipt=receipt, info_extension=info_extension,
                                                     return_info=return_info, user_notification=user_notification,
                                                     rejection_info=rejection_info, update_time=update_time,
                                                     line_item_updates=line_item_updates,
                                                     fulfillment_info=fulfillment_info, total_price=total_price,
                                                     in_transit_info=in_transit_info, action_order_id=action_order_id,
                                                     cancellation_info=cancellation_info, order_state=order_state,
                                                     google_order_id=google_order_id,
                                                     order_management_actions_list=order_management_actions_list)
        return self['richResponse']

    def add_media_response(self, media_type: MediaType, media_objects: MediaObject) -> RichResponse:
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['add_media_response(media_type=media_type, media_objects)
        return self['richResponse']

    def add_suggestions(self, titles) -> RichResponse:
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_suggestions(titles)
        return self['richResponse']

    def add_link_out_suggestion(self, url: str, destination_name: str) -> RichResponse:
        if self['richResponse'] is None:
            self['richResponse'] = RichResponse()
        self['richResponse'].add_link_out_suggestion(url=url, destination_name=destination_name)
        return self['richResponse']
