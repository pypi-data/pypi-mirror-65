class Image(dict):
    """
    {
      "imageUri": string,
      "accessibilityText": string
    }
    """

    def __init__(self, image_uri: str = '', accessibility_text: str = ''):
        super().__init__()

        if image_uri is not None:
            self['imageUri'] = image_uri
        if accessibility_text is not None:
            self['accessibilityText'] = accessibility_text
