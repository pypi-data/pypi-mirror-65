from typing import List
from .Cell import Cell


class Row(dict):
    """
    {
      "cells": [
        {
          object(Cell)
        }
      ],
      "dividerAfter": boolean
    }
    """

    def __init__(self, divider_after: bool = False, cells: Cell = None):
        super().__init__()
        if cells is None:
            cells = []

        self['dividerAfter'] = divider_after
        self['cells'] = cells

    def add_cells(self, cells: Cell) -> List[Cell]:
        for item in cells:
            assert isinstance(item, Cell)
            self['cells'].append(item)

        return self['cells']

    def add_cell(self, text: str) -> Cell:
        cell = Cell(text=text)
        self['cells'].append(cell)

        return cell
