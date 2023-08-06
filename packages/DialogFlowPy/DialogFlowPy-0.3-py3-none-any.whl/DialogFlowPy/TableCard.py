from typing import List

from DialogFlowPy import HorizontalAlignment

from DialogFlowPy.Button import Button
from DialogFlowPy.ColumnProperties import ColumnProperties
from DialogFlowPy.Image import Image
from DialogFlowPy.OpenUriAction import OpenUriAction
from DialogFlowPy.TableCardCell import TableCardCell
from DialogFlowPy.TableCardRow import TableCardRow


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
                 rows: List[TableCardRow], buttons: List[Button]):
        super().__init__()

        self['title'] = title
        self['subtitle'] = subtitle
        self['image'] = image
        self['columnProperties'] = column_properties
        self['rows'] = rows
        self['buttons'] = buttons

    @property
    def title(self):
        return self.get('title')

    @title.setter
    def title(self, title: str):
        self['title'] = title

    @property
    def subtitle(self):
        return self.get('subtitle')

    @subtitle.setter
    def subtitle(self, subtitle: str):
        self['subtitle'] = subtitle

    @property
    def image(self):
        return self.get('image')

    @image.setter
    def image(self, image: Image):
        self['image'] = image

    def add_image(self, image_uri: str, accessibility_text: str = '') -> Image:
        self.image = Image(image_uri=image_uri, accessibility_text=accessibility_text)
        return self.image

    @property
    def column_properties(self):
        return self.get('columnProperties')

    @column_properties.setter
    def column_properties(self, column_properties: ColumnProperties):
        self['columnProperties'] = column_properties

    def add_column_properties(self, column_properties: ColumnProperties) -> List[ColumnProperties]:
        for item in column_properties:
            assert isinstance(item, ColumnProperties)
            self['columnProperties'].append(item)
        return self['columnProperties']

    def add_column_property(self, header: str, horizontal_alignment: HorizontalAlignment) -> ColumnProperties:
        column_property = ColumnProperties(header=header, horizontal_alignment=horizontal_alignment)
        self['columnProperties'].append(column_property)
        return column_property

    @property
    def rows(self):
        return self.get('rows')

    @rows.setter
    def rows(self, rows_list: TableCardRow):
        self.rows = rows_list

    def add_rows(self, rows: TableCardRow) -> List[TableCardRow]:
        for item in rows:
            assert isinstance(item, TableCardRow)
            self.rows.append(item)
        return self.rows

    def add_row(self, divider_after: bool = False, cells: TableCardCell = None) -> TableCardRow:
        if cells is None:
            cells = []
        row = TableCardRow(divider_after=divider_after, table_card_cells=cells)
        self.rows.append(row)
        return row

    @property
    def buttons(self):
        return self.get('buttons')

    @buttons.setter
    def buttons(self, buttons_list):
        self['buttons'] = buttons_list

    def add_buttons(self, buttons) -> List[Button]:
        for item in buttons:
            assert isinstance(item, Button)
            self.buttons.append(item)

        return self.buttons

    def add_button(self, title: str, uri: str) -> Button:
        assert isinstance(title, str)
        assert isinstance(uri, str)

        self.buttons.append(Button(title=title, open_uri_action=OpenUriAction(uri=uri)))

        return self.buttons
