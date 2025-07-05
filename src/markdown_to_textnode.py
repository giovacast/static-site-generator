from textnode import TextType, TextNode
from extract_from_mkdwn import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # Analyze every node in the old_nodes list to see if the text in any of 
    # them contains the delimiter passed on the function.
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        elif delimiter in old_node.text:
            if old_node.text.count(delimiter) % 2 != 0:
                raise ValueError(f"Unclosed delimiter '{delimiter}' "
                                f"in text: {old_node.text}")
            parts = old_node.text.split(delimiter)
            temp_nodes = []
            for i, part in enumerate(parts):
                if part: #Skip empty parts.
                        node_type = text_type if i % 2 == 1 else TextType.TEXT
                        temp_nodes.append(TextNode(part, node_type))
            new_nodes.extend(temp_nodes)
        else:
            new_nodes.append(old_node)  # No delimiter, keep as-is     
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise TypeError("TypeError: node needs to be a TextNode.")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        image = extract_markdown_images(old_node.text)
        if not image:
             new_nodes.append(old_node)
             continue
        
        temp_nodes = []
        remaining_text = old_node.text
        for image_alt, image_link in image:
            # Split on current image
            parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if parts[0]:
                temp_nodes.append(TextNode(parts[0], TextType.TEXT))
            # Add image node
            temp_nodes.append(TextNode(image_alt, TextType.IMAGE, 
                                               image_link))
            # Update remaining text
            remaining_text = parts[1]
            # Add final text after last image
        if remaining_text:
                temp_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(temp_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise TypeError("TypeError: node needs to be a TextNode.")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link = extract_markdown_links(old_node.text)
        if not link:
            new_nodes.append(old_node)
            continue

        temp_nodes = []
        remaining_text = old_node.text
        for anchor_txt, url in link:
            # Split on current link
            parts = remaining_text.split(f"[{anchor_txt}]({url})", 1)
            if parts[0]:
                temp_nodes.append(TextNode(parts[0], TextType.TEXT))
            # Add link node    
            temp_nodes.append(TextNode(anchor_txt, TextType.LINK, url))
            # Update remaining text
            remaining_text = parts[1]
        # Add final text after last link
        if remaining_text:
            temp_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(temp_nodes)
    return new_nodes