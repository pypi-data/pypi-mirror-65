class Image(dict):
    """{
            "smallImageUrl": "https://url-to-small-card-image...",
            "largeImageUrl": "https://url-to-large-card-image..."
          }
    """

    def __init__(self, small_image_url: str = None, large_image_url: str = None) -> None:

        super(Image, self).__init__()

        if small_image_url is not None:
            self['smallImageUrl'] = small_image_url

        if large_image_url is not None:
            self['largeImageUrl'] = large_image_url
