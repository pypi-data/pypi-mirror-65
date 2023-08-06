from DialogFlowPy import HorizontalAlignment


class ColumnProperties(dict):
    """
    {
      "header": string,
      "horizontalAlignment": enum(HorizontalAlignment)
    }
    """

    def __init__(self, header: str, horizontal_alignment: HorizontalAlignment):
        super(ColumnProperties, self).__init__()

        self.header = header
        self.horizontal_alignment = horizontal_alignment

    @property
    def header(self):
        return self.get('header')

    @header.setter
    def header(self, header: str):
        self['header'] = header

    @property
    def horizontal_alignment(self):
        return HorizontalAlignment(self.get('horizontalAlignment'))

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment: HorizontalAlignment):
        self['horizontalAlignment'] = horizontal_alignment.name
