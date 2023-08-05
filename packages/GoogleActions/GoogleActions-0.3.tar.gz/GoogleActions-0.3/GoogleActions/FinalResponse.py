from typing import List
from .RichResponse import RichResponse
from .LinkOutSuggestion import LinkOutSuggestion
from .Suggestion import Suggestion
from .Item import Item


class FinalResponse(dict):
    """
    {
      "richResponse": {
        object(RichResponse)
      },
    }
    """

    def __init__(self, rich_response: RichResponse = None):
        super().__init__()

        self['richResponse'] = rich_response

    def add_rich_response(self, items_list: List[Item] = None, suggestions_list: List[Suggestion] = None,
                          link_out_suggestion: LinkOutSuggestion = None) -> RichResponse:
        self['richResponse'] = RichResponse(item_list=items_list, suggestions=suggestions_list,
                                            link_out_suggestion=link_out_suggestion)

        return self['richResponse']
