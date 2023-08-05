from . import CarouselItem
from . import ImageDisplayOptions
from . import MediaType
from .BasicCard import BasicCard
from .Button import Button
from .CarouselBrowse import CarouselBrowse
from .Image import Image
from .MediaResponse import MediaResponse
from .SimpleResponse import SimpleResponse
from .StructuredResponse import StructuredResponse
from .TableCard import TableCard


class Item(dict):
    """
    {

      // Union field item can be only one of the following:
      "simpleResponse": {
        object(SimpleResponse)
      },
      "basicCard": {
        object(BasicCard)
      },
      "structuredResponse": {
        object(StructuredResponse)
      },
      "mediaResponse": {
        object(MediaResponse)
      },
      "carouselBrowse": {
        object(CarouselBrowse)
      },
      "tableCard": {
        object(TableCard)
      }
      // End of list of possible types for union field item.
    }
    """

    def __init__(self, member_object=None):
        super().__init__()

        assert isinstance(member_object, (StructuredResponse, SimpleResponse, BasicCard, MediaResponse,
                                          CarouselBrowse, TableCard))
        self.add_member_object(member_object)

    def add_member_object(self, member_object):
        if isinstance(member_object, SimpleResponse):
            self['simpleResponse'] = member_object
        elif isinstance(member_object, BasicCard):
            self['basicCard'] = member_object
        elif isinstance(member_object, StructuredResponse):
            self['structuredResponse'] = member_object
        elif isinstance(member_object, MediaResponse):
            self['mediaResponse'] = member_object
        elif isinstance(member_object, CarouselBrowse):
            self['carouselBrowse'] = member_object
        elif isinstance(member_object, TableCard):
            self['tableCard'] = member_object

        return self

    def clear_item(self):
        for item in self:
            self.pop(item)

    @property
    def simple_response(self):
        return self.get('simpleResponse')

    @simple_response.setter
    def simple_response(self, simple_response: SimpleResponse):
        self.clear_item()
        self['simpleResponse'] = simple_response

    @simple_response.deleter
    def simple_response(self):
        self.pop('simpleResponse')

    def add_simple_response(self, text_to_speech: str, ssml: str, display_text: str) -> SimpleResponse:
        self.clear_item()
        self['simpleResponse'] = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml,
                                                display_text=display_text)

        return self['simpleResponse']

    @property
    def basic_card(self):
        return self.get('basicCard')

    @basic_card.setter
    def basic_card(self, basic_card: BasicCard):
        self.clear_item()
        self['basicCard'] = basic_card

    @basic_card.deleter
    def basic_card(self):
        self.pop('basicCard')

    def add_basic_card(self, title: str = '', formatted_text: str = '', subtitle: str = '', image: Image = None,
                       image_display_options: ImageDisplayOptions = None, buttons: Button = None) -> BasicCard:
        if buttons is None:
            buttons = []
        self.clear_item()
        self['basicCard'] = BasicCard(title=title, formatted_text=formatted_text,
                                      subtitle=subtitle, image=image,
                                      image_display_options=image_display_options, buttons=buttons)

        return self['basicCard']

    @property
    def structured_response(self):
        return self.get('structuredResponse')

    @structured_response.setter
    def structured_response(self, value):
        self.clear_item()
        self['structuredResponse'] = value

    @structured_response.deleter
    def structured_response(self):
        self.pop('structuredResponse')

    @property
    def media_response(self):
        return self.get('mediaResponse')

    @media_response.setter
    def media_response(self, value):
        self.clear_item()
        self['mediaResponse'] = value

    @media_response.deleter
    def media_response(self):
        self.pop('mediaResponse')

    def add_media_response(self, media_type: MediaType, media_objects) -> MediaResponse:
        self['mediaResponse'] = MediaResponse(media_type=media_type, media_objects=media_objects)

        return self['mediaResponse']

    @property
    def carousel_browse(self):
        return self.get('carouselBrowse')

    @carousel_browse.setter
    def carousel_browse(self, value):
        self.clear_item()
        self['carouselBrowse'] = value

    @carousel_browse.deleter
    def carousel_browse(self):
        self.pop('carouselBrowse')

    def add_carousel_browse(self, image_display_options: ImageDisplayOptions, items: CarouselItem):
        self['carouselBrowse'] = CarouselBrowse(image_display_options=image_display_options,
                                                carousel_browse_items=items)

        return self['carouselBrowse']

    @property
    def table_card(self):
        return self.get('tableCard')

    @table_card.setter
    def table_card(self, value):
        self.clear_item()
        self['tableCard'] = value

    @table_card.deleter
    def table_card(self):
        self.pop('tableCard')

    def add_table_card(self, title: str, subtitle: str, image: Image, column_properties, rows, buttons):
        self['tableCard'] = TableCard(title=title, subtitle=subtitle, image=image, column_properties=column_properties,
                                      rows=rows, buttons=buttons)
