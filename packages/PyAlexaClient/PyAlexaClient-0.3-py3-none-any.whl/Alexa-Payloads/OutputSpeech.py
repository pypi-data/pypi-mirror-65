class OutputSpeech(dict):
    """
    {
          "type": "PlainText"/"SSML",
          "text": "Plain text string to speak",
          "ssml": "<speak>SSML text string to speak</speak>"
        }
    """

    def __init__(self, speech_type: str = 'PlainText', text: str = None, ssml: str = None):
        
        super(OutputSpeech, self).__init__()

        assert speech_type in ('PlainText', 'SSML')
        if text is not None:
            self['text'] = text
        if ssml is not None:
            self['ssml'] = ssml
        if speech_type is not None:
            self['type'] = speech_type
