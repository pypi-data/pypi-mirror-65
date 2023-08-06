from typing import Optional

from .Image import Image


class Card(dict):
    """
    {
          'type': 'Standard/LinkAccount/Simple',
          'title': 'Title of the card',
          'content': 'Content of a simple card',
          'text': 'Text content for a standard card',
          'image': AlexaImageObject
        }
    """

    def __init__(self, card_type: str = 'Standard', title: Optional[str] = '', content: Optional[str] = '',
                 text: Optional[str] = '', image: Image = None):
        super(Card, self).__init__()

        if image is None:
            image = {}

        assert card_type in ('Standard', 'LinkAccount', 'Simple')
        self['title'] = title
        self['content'] = content
        self['type'] = card_type
        self['text'] = text
        self['image'] = image
