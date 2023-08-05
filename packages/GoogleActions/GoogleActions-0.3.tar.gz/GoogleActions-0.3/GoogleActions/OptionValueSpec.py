from typing import Union
from .SimpleSelect import SimpleSelect
from .ListSelect import ListSelect
from .CarouselSelect import CarouselSelect


class OptionValueSpec(dict):
    """
    {

      // Union field select can be only one of the following:
      'simpleSelect': {
        object(SimpleSelect)
      },
      'listSelect': {
        object(ListSelect)
      },
      'carouselSelect': {
        object(CarouselSelect)
      }
      // End of list of possible types for union field select.
    }
    """

    def __init__(self, option_object: Union[SimpleSelect, ListSelect, CarouselSelect]):
        super().__init__()

        if isinstance(option_object, SimpleSelect):
            self['simpleSelect'] = option_object
        elif isinstance(option_object, ListSelect):
            self['listSelect'] = option_object
        elif isinstance(option_object, CarouselSelect):
            self['carouselSelect'] = option_object
