import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        """Tests that passing an empty string returns an empty list."""
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_whitespace_only(self):
        """Tests that passing a series of newlines is treated as an empty 
        string and returns an empty list."""
        blocks = markdown_to_blocks("    \n\n \t ")
        self.assertEqual(blocks, [])

    def test_multiple_newlines_between_blocks(self):
        """Tests that multiple newlines between blocks are handled correctly."""
        md = "This is a block\n\n\n\nThis is another block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a block", "This is another block"])
    
    def test_leading_and_trailing_whitespace(self):
        """Test that whitespace/newlines at the start and end are stripped."""
        md = """
        
        This is the first paragraph.
        
        This is the second.

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is the first paragraph.", "This is the second."],
        )

    def test_invalid_input_type(self):
        """Test that non-string input raises a TypeError."""
        with self.assertRaises(TypeError):
            markdown_to_blocks(123)
        with self.assertRaises(TypeError):
            markdown_to_blocks(None)
        with self.assertRaises(TypeError):
            markdown_to_blocks(["list", "of", "strings"])