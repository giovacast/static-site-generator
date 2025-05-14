from enum import Enum

class TextType(Enum):
    """A class to represent all the different types of inline text"""
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """checks if all of the properties of two textnode objects
        are equal."""
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)

    def __repr__(self):
        """returns a string representation of the textnode object."""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"