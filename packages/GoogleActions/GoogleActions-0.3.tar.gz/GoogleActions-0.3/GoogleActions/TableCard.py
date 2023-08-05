from typing import List
from .OpenUrlAction import OpenUrlAction
from .Image import Image
from .Button import Button
from .ColumnProperties import ColumnProperties
from .Row import Row
from .Cell import Cell
from . import HorizontalAlignment


class TableCard(dict):
    """
    {
      "title": string,
      "subtitle": string,
      "image": {
        object(Image)
      },
      "columnProperties": [
        {
          object(ColumnProperties)
        }
      ],
      "rows": [
        {
          object(Row)
        }
      ],
      "buttons": [
        {
          object(Button)
        }
      ]
    }
    """

    def __init__(self, title: str, subtitle: str, image: Image, column_properties: List[ColumnProperties],
                 rows: List[Row], buttons: List[Button]):
        super().__init__()

        self['title'] = title
        self['subtitle'] = subtitle
        self['image'] = image
        self['columnProperties'] = column_properties
        self['rows'] = rows
        self['buttons'] = buttons

    def add_image(self, url: str, accessibility_text: str = '', height: int = 0, width: int = 0) -> Image:
        self['image'] = Image(url=url, accessibility_text=accessibility_text, height=height, width=width)
        return self['image']

    def add_column_properties(self, column_properties: ColumnProperties) -> List[ColumnProperties]:
        for item in column_properties:
            assert isinstance(item, ColumnProperties)
            self['columnProperties'].append(item)
        return self['columnProperties']

    def add_column_property(self, header: str, horizontal_alignment: HorizontalAlignment) -> ColumnProperties:
        column_property = ColumnProperties(header=header, horizontal_alignment=horizontal_alignment)
        self['columnProperties'].append(column_property)
        return column_property

    def add_rows(self, rows: Row) -> List[Row]:
        for item in rows:
            assert isinstance(item, Row)
            self['rows'].append(item)
        return self['rows']

    def add_row(self, divider_after: bool = False, cells: Cell = None) -> Row:
        if cells is None:
            cells = []
        row = Row(divider_after=divider_after, cells=cells)
        self['rows'].append(row)
        return row

    def add_buttons(self, buttons) -> List[Button]:
        for item in buttons:
            assert isinstance(item, Button)
            self['buttons'].append(item)

        return self['buttons']

    def add_button(self, title: str, url: str) -> Button:
        assert isinstance(title, str)
        assert isinstance(url, str)

        self['button'] = Button(title=title, open_url_action=OpenUrlAction(action_url=url))

        return self['button']
