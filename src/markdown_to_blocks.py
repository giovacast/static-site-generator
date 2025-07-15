def markdown_to_blocks(markdown):
    """This function takes a raw markdown string (representing a full document) 
    as input and returns a list of "block" strings."""

    if not isinstance(markdown, str):  
        raise TypeError("Input must be a string")

    current_block_lines = []
    blocks = []

    all_lines = markdown.split("\n")

    for line in all_lines:
        if line.strip():
            current_block_lines.append(line.strip())             
        else:
            # If the line is blank, it marks the end of a block
            if current_block_lines:
                # Join the lines of the completed block and add it to our final list
                blocks.append("\n".join(current_block_lines))

                # Reset the temporary list for the next block
                current_block_lines = []


        # After the loop, there might be a final block that hasn't been added yet
    if current_block_lines:
        blocks.append("\n".join(current_block_lines))

    return blocks