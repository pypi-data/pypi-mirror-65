from .OptionInfo import OptionInfo
from typing import List


class SelectItem(dict):
    """
    {
      'optionInfo': object(optioninfo),
      'title': string
    }
    """

    def __init__(self, title: str = '', option_info: OptionInfo = None):
        super().__init__()

        self['optionInfo'] = option_info
        self['title'] = title

    def add_option_info(self, key: str, synonyms: List[str]) -> OptionInfo:
        self['optionInfo'] = OptionInfo(key=key, synonyms=synonyms)
        return self['optionInfo']
