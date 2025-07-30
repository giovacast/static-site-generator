import unittest
from block_type_identifier import BlockType, block_to_block_type

class TestBlockTypeIdentifier(unittest.TestCase):
    """This class contains all tests for the block_to_block_type
    function."""

    def test_paragraph(self):
        """Tests that the function identifies a markdown paragraph."""
        block = """
                This is a simple paragraph of text to make sure our function
                can identify it.
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading(self):
        """Tests that the function identifies a heading."""
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        """Tests that the function returns BlockType.PARAGRAPH 
        when a block that starts with more than 6 "#"  is passed."""
        block = "####### "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_empty_heading(self):
        """Tests that the function returns BlockType.HEADING 
        when only a "# " is passed in a block."""
        block = "# "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_no_space(self):
        """Tests that when a block is passed starting with a "#" immediately 
        followed by text with no space in between, the function returns
        BlockType.PARAGRAPH."""
        block = "#Not a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        """Tests that the function identifies an unordered list."""
        block = """
                - This is an unordered list.
                - It has different items on every line.
                - Like this other item.        
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        """Tests that the function identifies an ordered list."""
        block = """
                1. This is an ordered list
                2. It implies that there's some sort of sequence
                3. It's treated differently than an unordered list
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_quote(self):
        """Tests that the function can identify a block of quotes."""
        block = """
                > This is a quote.
                >We know it's a quote in markdown because it starts with a ">"
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_code(self):
        """Tests that the function can identify a block of code."""
        block = """
                ```
                This is a block of <code> apparently
                and we want to make sure that the function can identify it
                as such
                ```
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_unordered_list_with_blank_line(self):
        """Tests that an unordered list with a blank line is still identified correctly."""
        block = """
                - Item one
                 
                - Item two
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_with_extra_whitespace(self):
        """Tests that an unordered list with extra/trailing whitespace is identified."""
        block = """
                - Item one  
                -  Item two    
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_with_blank_line(self):
        """Tests that an ordered list with a blank line is still identified correctly."""
        block = """
                1. Item one
                
                2. Item two
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_with_extra_whitespace(self):
        """Tests that an ordered list with extra/trailing whitespace is identified."""
        block = """
                1. Item one  
                2.  Item two    
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_code_block_empty(self):
        """Tests that an empty code block is identified as code."""
        block = """
                ```
                ```
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_block_with_language_hint(self):
        """Tests that a code block with a language hint is identified as code."""
        block = """
                ```python
                print("Hello, world!")
                ```
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_block_non_matching_backticks(self):
        """Tests that a code block with non-matching backtick 
        numbers is a paragraph."""
        block = """
                ```
                This is not a proper code block
                ``
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_missing_space(self):
        """Tests that a list-like block without spaces after - is a paragraph."""
        block = """
                -Item one
                -Item two
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_mixed_block_list_and_paragraph(self):
        """Tests that a block mixing list and paragraph lines is a paragraph."""
        block = """
                - Item one
                This is a paragraph line
                - Item two
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_only_whitespace(self):
        """Tests that a block with only whitespace is a paragraph."""
        block = """
                   
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_inconsistent_indentation(self):
        """Tests that a block with inconsistent indentation is still identified."""
        block = """
                    - Item one
                - Item two
                        - Item three
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_single_item_unordered_list(self):
        """Tests that a single-item unordered list is identified correctly."""
        block = "- Single item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_single_item_ordered_list(self):
        """Tests that a single-item ordered list is identified correctly."""
        block = "1. Single item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_long_unordered_list(self):
        """Tests that a long unordered list is identified correctly."""
        block = "\n".join(f"- Item {i}" for i in range(1, 21))
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_paragraph_with_special_chars(self):
        """Tests that a paragraph with special characters is not misidentified."""
        block = """
                This paragraph has # - 1. special chars
                but should not be a heading or list
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_with_space(self):
        """Tests that a quote with space after > is identified correctly."""
        block = """
                > quote
                > another quote
        """
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)