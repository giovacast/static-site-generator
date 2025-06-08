from textnode import TextType, TextNode

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


    