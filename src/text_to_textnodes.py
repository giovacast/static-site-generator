from textnode import TextType, TextNode
from markdown_to_textnode import split_nodes_delimiter, split_nodes_image, \
split_nodes_link

def text_to_textnodes(text):
    # Use the string passed to the function to create a TextNode with
    # TextType.TEXT
    nodes = [TextNode(text, TextType.TEXT)]

    # Call every function iteratively on the same list:
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes