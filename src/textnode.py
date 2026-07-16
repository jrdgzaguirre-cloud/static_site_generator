from enum import Enum

class TextType(Enum):
    PLAIN = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str,  text_type: TextType, url: str = None,):
        self.text = text
        self.url = url
        self.text_type = text_type

    def __eq__(self, other):
        if self.text == other.text and self.url == other.url and self.text_type == other.text_type:
            return True
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'