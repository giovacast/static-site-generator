from textnode import TextType, TextNode  
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text is None:
        raise ValueError("TextNode.text cannot be None")
    
    html_types = {
                  TextType.TEXT: None, 
                  TextType.BOLD: "b",
                  TextType.ITALIC: "i",
                  TextType.CODE: "code",
                  TextType.LINK: "a",
                  TextType.IMAGE: "img",
                  }

    
    if text_node.text_type not in html_types:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")
    
    props = {}
    value = text_node.text
    if text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("TextType.LINK requires a valid URL")
        props = {"href": text_node.url}
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("TextType.LINK requires a valid URL")
        props = {"src": text_node.url, "alt": text_node.text}
        value = None
    
    return LeafNode(html_types[text_node.text_type], 
                    value, props)