class SimpleResponse(dict):
    """
    {
      "textToSpeech": string,
      "ssml": string,
      "displayText": string,
    }
    """

    def __init__(self, text_to_speech: str = '', ssml: str = '', display_text: str = ''):
        super().__init__()

        if text_to_speech is not None:
            self['textToSpeech'] = text_to_speech
        if ssml is not None:
            self['ssml'] = ssml
        if display_text is not None:
            self['displayText'] = display_text
