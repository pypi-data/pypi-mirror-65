class Image(dict):
    """
    {
      "url": string,
      "accessibilityText": string,
      "height": number,
      "width": number,
    }
    """

    def __init__(self, url: str = '', accessibility_text: str = '', height: int = 0, width: int = 0):
        super(Image, self).__init__()

        if url is not None:
            self['url'] = url
        if accessibility_text is not None:
            self['accessibilityText'] = accessibility_text
        if height is not None:
            self['height'] = height
        if width is not None:
            self['width'] = width
