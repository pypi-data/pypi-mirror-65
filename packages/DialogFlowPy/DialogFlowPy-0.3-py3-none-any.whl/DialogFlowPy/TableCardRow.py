from typing import List

from DialogFlowPy.TableCardCell import TableCardCell


class TableCardRow(dict):
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

    def __init__(self, divider_after: bool = False, table_card_cells: List[TableCardCell] = None):
        super().__init__()
        if table_card_cells is None:
            table_card_cells = []

        self.divider_after = divider_after
        self.table_card_cells = table_card_cells

    @property
    def divider_after(self):
        return self.get('dividerAfter')

    @divider_after.setter
    def divider_after(self, divider_after: bool):
        self['dividerAfter'] = divider_after

    @property
    def table_card_cells(self):
        return self.get('cells')

    @table_card_cells.setter
    def table_card_cells(self, table_card_list):
        self['cells'] = table_card_list

    def add_cells(self, cells: TableCardCell) -> List[TableCardCell]:
        for item in cells:
            assert isinstance(item, TableCardCell)
            self['cells'].append(item)

        return self['cells']

    def add_cell(self, text: str) -> TableCardCell:
        cell = TableCardCell(text=text)
        self['cells'].append(cell)

        return cell
