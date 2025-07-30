from markdown_to_blocks import markdown_to_blocks
from block_type_identifier import BlockType, block_to_block_type
from htmlnode import ParentNode, LeafNode
from text_to_textnodes import text_to_textnodes
from node_converter import text_node_to_html_node
import re
from textnode import TextNode, TextType

def text_to_children(block):
    """Takes a block of markdown text and returns a list of LeafNodes based on
        the different types of inline text it finds."""
    nodes = text_to_textnodes(block)
    return [text_node_to_html_node(node) for node in nodes]

def block_to_paragraph_node(block):
    """Takes a markdown paragraph and returns a ParentNode 
        with it's children."""
    child_nodes = text_to_children(block)
    return ParentNode("p", child_nodes)

def block_to_heading(block):
    """Converts a heading block into an HTMLNode."""
    match = re.match(r"^(#+)\s*(.*)$", block.lstrip())
    level = len(match.group(1))
    return ParentNode(f"h{level}", text_to_children(match.group(2)))

def block_to_quote(block):
    """Converts a quote block into an HTMLNode."""
    lines = ([line.lstrip("> ").strip() for line in block.split("\n") 
              if line.strip()])
    return ParentNode("blockquote", text_to_children("\n".join(lines)))

def block_to_list_node(block, block_type):
    """Converts a list block to an HTMLNode."""
    lines = block.split("\n")
    child_nodes = []
    prefix = "- " if block_type == BlockType.UNORDERED_LIST else r"\d+\. "
    for line in lines:
        if line.strip():
            match = re.match(rf"^\s*{prefix}(.*)$", line)
            if match:
                content = match.group(1).strip()
                child_nodes.append(ParentNode("li", text_to_children(content)))
    if not child_nodes:
        return ParentNode("ul" if block_type == BlockType.UNORDERED_LIST 
                          else "ol", [ParentNode("li", [LeafNode(None, " ")])])
    return ParentNode("ul" if block_type == BlockType.UNORDERED_LIST else "ol",
                      child_nodes)

def block_to_code_node(block):
    """Converts a code block to an HTMLNode."""
    lines = block.split("\n")[1:-1]
    # Filter empty lines for consistency
    lines = [line for line in lines if line.strip()]
    # Add trailing newline to match test expectation
    content = "\n".join(lines) + "\n" if lines else " "
    html_node = text_node_to_html_node(TextNode(content, TextType.CODE))
    return ParentNode("pre", [html_node])

def markdown_to_html_node(markdown):
    """This function takes a markdown document and converts it into a single
    parent HTMLNode."""
    # Split the markdown into blocks 
    blocks = markdown_to_blocks(markdown)

    parent_nodes = []
    # Loop over each block:
    for block in blocks:
        #     Determine the type of block 
        block_type = block_to_block_type(block)
        # Based on the type of block, create a new HTMLNode with the proper data
        if block_type == BlockType.PARAGRAPH:
            parent_nodes.append(block_to_paragraph_node(block))
        elif block_type == BlockType.HEADING:
            parent_nodes.append(block_to_heading(block))
        elif block_type == BlockType.QUOTE:
            parent_nodes.append(block_to_quote(block))
        elif block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            parent_nodes.append(block_to_list_node(block, block_type))
        elif block_type == BlockType.CODE:
            parent_nodes.append(block_to_code_node(block))

    return(ParentNode("div", parent_nodes))