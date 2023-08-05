from typing import List

from . import ImageDisplayOptions, MediaType
from .BasicCard import BasicCard
from .Button import Button
from .CarouselBrowse import CarouselBrowse
from .CarouselBrowseItem import CarouselBrowseItem
from .Image import Image
from .Item import Item
from .LinkOutSuggestion import LinkOutSuggestion
from .MediaObject import MediaObject
from .MediaResponse import MediaResponse
from .OrderUpdate import OrderUpdate
from .SimpleResponse import SimpleResponse
from .StructuredResponse import StructuredResponse
from .Suggestion import Suggestion
from .TableCard import TableCard


class RichResponse(dict):
    """
    {
      "items": [
        {
          object(Item)
        }
      ],
      "suggestions": [
        {
          object(Suggestion)
        }
      ],
      "linkOutSuggestion": {
        object(LinkOutSuggestion)
      },
    }
    """

    def __init__(self, item_list: list = None, suggestions: list = None, link_out_suggestion: LinkOutSuggestion = None):
        super().__init__()

        if item_list is not None:
            if self.check_structure_validity(item_list):
                self['items'] = item_list
        else:
            self['items'] = []

        if suggestions is not None:
            self['suggestions'] = suggestions
        else:
            self['suggestions'] = []

        self['linkOutSuggestion'] = link_out_suggestion or dict()

    @property
    def item_list(self):
        return self.get('items')

    @item_list.setter
    def item_list(self, item_list):
        self['items'] = item_list

    def add_items(self, *items) -> List[Item]:
        print('adding items: ', items)
        temp_item_list = []
        temp_item_list.extend(self['items'])
        for item in items:
            print('adding to temp_item_list: ', item)
            temp_item_list.append(item)

        print('checking structure_validity of temp_item_list: ', temp_item_list)
        if self.check_structure_validity(temp_item_list):
            print('extending items_list')
            self['items'].extend(items)

        return self['items']

    @property
    def suggestions(self):
        return self.get('suggestions')

    @suggestions.setter
    def suggestions(self, suggestion_list):
        self['suggestions'] = suggestion_list

    def add_suggestions(self, titles: str) -> List[Suggestion]:
        print('adding suggestion: ', titles)

        for title in titles:
            self['suggestions'].append(Suggestion(title=title))

        return self['suggestions']

    @property
    def link_out_suggestion(self):
        return self.get('linkOutSuggestion')

    @link_out_suggestion.setter
    def link_out_suggestion(self, link_out_suggestion):
        self['linkOutSuggestion'] = link_out_suggestion

    def add_link_out_suggestion(self, url: str, destination_name: str) -> LinkOutSuggestion:
        print('adding link_out_suggestion ', url, destination_name)

        self['linkOutSuggestion'] = LinkOutSuggestion(url=url, destination_name=destination_name)

        return self['linkOutSuggestion']

    def add_simple_response(self, text_to_speech: str, ssml: str, display_text: str) -> Item:
        print('adding simple response to')
        print('items_list: ', self['items'])

        item = Item(SimpleResponse(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text))
        self.add_items(item)
        print('items_list: ', self['items'])

        return item

    def add_basic_card(self, title: str, formatted_text: str, subtitle: str, image_url: str,
                       image_text: str, image_height: int, image_width: int,
                       image_display_options: ImageDisplayOptions, buttons: List[Button]) -> Item:
        print('adding basic card')

        item = Item(BasicCard(title=title, formatted_text=formatted_text,
                              subtitle=subtitle, image=Image(url=image_url,
                                                             accessibility_text=image_text,
                                                             height=image_height,
                                                             width=image_width),
                              image_display_options=image_display_options,
                              buttons=buttons))
        self.add_items(item)
        return item

    def add_structured_response(self, receipt=None, info_extension=None,
                                return_info=None,
                                user_notification=None, rejection_info=None, update_time=None,
                                line_item_updates=None, fulfillment_info=None,
                                total_price=None,
                                in_transit_info=None, action_order_id=None,
                                cancellation_info=None,
                                order_state=None, google_order_id=None,
                                order_management_actions_list=None) -> Item:
        print('adding structured_response')

        item = Item(StructuredResponse(
            order_update=OrderUpdate(receipt=receipt, info_extension=info_extension, return_info=return_info,
                                     user_notification=user_notification, rejection_info=rejection_info,
                                     update_time=update_time, line_item_updates=line_item_updates,
                                     fulfillment_info=fulfillment_info, total_price=total_price,
                                     in_transit_info=in_transit_info, action_order_id=action_order_id,
                                     cancellation_info=cancellation_info, order_state=order_state,
                                     google_order_id=google_order_id,
                                     order_management_actions_list=order_management_actions_list)))
        self.add_items(item)
        return item

    def add_media_response(self, media_type: MediaType, media_objects: List[MediaObject]) -> Item:
        print('adding media response: ', media_type, media_objects)

        item = Item(MediaResponse(media_type=media_type, media_objects=media_objects))
        self.add_items(item)

        return item

    def add_carousel_browse(self, image_display_options: ImageDisplayOptions,
                            carousel_browse_items: List[CarouselBrowseItem]):
        item = Item(
            CarouselBrowse(image_display_options=image_display_options, carousel_browse_items=carousel_browse_items))
        self.add_items(item)
        return item

    def add_table_card(self, title: str, subtitle: str, image_uri: str, accessibility_text: str, image_height: int,
                       image_width: int, column_properties, rows, buttons):
        item = Item(TableCard(title=title, subtitle=subtitle, image=Image(url=image_uri,
                                                                          accessibility_text=accessibility_text,
                                                                          height=image_height, width=image_width),
                              column_properties=column_properties,
                              rows=rows, buttons=buttons))

        self.add_items(item)

    @staticmethod
    def check_structure_validity(items_list: list) -> bool:
        print('checking structure validity for ', items_list)

        num_of_simple_responses = 0
        num_of_rich_responses = 0

        for item_object in items_list:
            print('item_object:', item_object)

            if item_object.get('simpleResponse') is not None:
                num_of_simple_responses += 1
            elif item_object.get('basicCard') is not None:
                num_of_rich_responses += 1
            elif item_object.get('structuredResponse') is not None:
                num_of_rich_responses += 1
            elif item_object.get('mediaResponse') is not None:
                num_of_rich_responses += 1
            elif item_object.get('HTMLResponse') is not None:
                num_of_rich_responses += 1
            elif item_object.get('carouselBrowse') is not None:
                num_of_rich_responses += 1
            elif item_object.get('tableCard') is not None:
                num_of_rich_responses += 1

        assert (items_list[0].get('simpleResponse'))

        assert (num_of_simple_responses <= 2)
        assert (num_of_rich_responses <= 1)
        print('all ok')

        return True
