from typing import List

from .OptionInfo import OptionInfo
from .SelectItem import SelectItem


class SimpleSelect(dict):
    """
    {
      'item_list': [
        {
          object(SelectItem)
        }
      ]
    }
    """

    def __init__(self, select_items: SelectItem):
        super().__init__()

        self['item_list'] = []
        for item in select_items:
            assert isinstance(item, SelectItem)
            self['item_list'].append(item)

    def add_select_items(self, select_items: SelectItem) -> List[SelectItem]:
        for item in select_items:
            assert isinstance(item, SelectItem)
            self['item_list'].append(item)
        return self['item_list']

    def add_select_item(self, key: str, title: str, synonyms: List[str]) -> SelectItem:
        select_item = SelectItem(title=title, option_info=OptionInfo(key=key, synonyms=synonyms))
        self['item_list'].append(select_item)
        return select_item
