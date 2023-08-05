"""Implementation of the Image CFX Structure."""
from .base import CFXStructure, load_basic


class Image(CFXStructure):
    """No official IPC-CFX description.

    image_data (str): A binary representation of the image.  #HACK: In the official IPC-CFX demo,
        this is supposed to be a bytes object. We chose to use a base64 encoded representation instead.
    mime_type (str): The MIME type of the binary image data contained by the ImageData property.
    """
    def __init__(self, **kwargs):
        self.image_data = load_basic(kwargs, "image_data", str, "")
        self.mime_type = load_basic(kwargs, "mime_type", str, "image/jpg")
