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

    def __init__(self, card_type: str = 'Standard', title: Optional[str] = None, content: Optional[str] = None,
                 text: Optional[str] = None, image: Optional[Image] = None):
        
        super(Card, self).__init__()

        if image is None:
            image = dict()

        assert card_type in ('Standard', 'LinkAccount', 'Simple')
        if title is not None:
            self['title'] = title
        if content is not None:
            self['content'] = content
        if content is not None:
            self['type'] = card_type
        if content is not None:
            self['text'] = text
        if content is not None:
            self['image'] = image
