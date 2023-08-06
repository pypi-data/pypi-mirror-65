class OutputSpeech(dict):
    """
    {
          "type": "PlainText"/"SSML",
          "text": "Plain text string to speak",
          "ssml": "<speak>SSML text string to speak</speak>"
        }
    """

    def __init__(self, speech_type: str = '', text: str = '', ssml: str = ''):
        super(OutputSpeech, self).__init__()

        assert speech_type in ('PlainText', 'SSML')
        self['text'] = text
        self['ssml'] = ssml
        self['type'] = speech_type
