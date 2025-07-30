from enum import Enum
import re

class BlockType(Enum):
    """An enum to represent all the different types of markdown blocks
       we'll be working with."""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE = "code"
    QUOTE = "quote"

def block_to_block_type(block):
    if not block.strip():
    # block is empty or only whitespace
        return BlockType.PARAGRAPH  

    lines = block.split("\n")
    processed_lines = [line.strip() for line in lines if line.strip()]
    
    if (re.match(r"#{1,6} ",
                 next(line for line in lines if line.strip()).lstrip())):
        return BlockType.HEADING
    elif all(line.startswith(">") for line in processed_lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in processed_lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{index + 1}. ") for index,
                line in enumerate(processed_lines)):
        return BlockType.ORDERED_LIST
    elif (
        processed_lines[0].strip().startswith("```") 
        and processed_lines[-1].strip().startswith("```") 
        and len(processed_lines) > 1):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH