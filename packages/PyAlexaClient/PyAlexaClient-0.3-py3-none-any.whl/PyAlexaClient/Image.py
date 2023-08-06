class Image(dict):
    """{
            "smallImageUrl": "https://url-to-small-card-image...",
            "largeImageUrl": "https://url-to-large-card-image..."
          }
    """

    def __init__(self, small_image_url: str = '', large_image_url: str = '') -> None:
        super(Image, self).__init__()

        self['smallImageUrl'] = small_image_url

        self['largeImageUrl'] = large_image_url
