import unittest
from textnode import TextType, TextNode
from markdown_to_text import split_nodes_delimiter

class TestMarkdowntoTextNode(unittest.TestCase):

    def test_delimiter_at_beginning(self):
        """This tests cases in which the delimeter is at the very beginning
            of the text."""
        node = [TextNode("**Important:** Save before quitting!", 
                              TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Important:", TextType.BOLD),
                                    TextNode(" Save before quitting!", 
                                    TextType.TEXT)])
    
    def test_delimeter_at_end(self):
        """This tests cases in which the delimeter is at the 
            very end of the text."""
        node = [
            TextNode("The final word in this text is **bolded**", 
                     TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [
            TextNode("The final word in this text is ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD)
        ]

    def test_delimeter_at_middle(self):
        """This tests cases in which the delimeter is not at the beginning of
            the string."""
        node = [TextNode("This: `print('Hello world')` is computer code.", 
                         TextType.TEXT)]

        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [
            TextNode("This: ", TextType.TEXT),
            TextNode("print('Hello world')", TextType.CODE),
            TextNode(" is computer code.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_unbalanced_delimiter(self):
        """This tests cases in which there's an unclosed delimeter and raises 
            a ValueError."""
        node = [TextNode("Hey! **Stop!", TextType.TEXT)]
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(str(e.exception), "Unclosed delimiter '**' in text: "
                         "Hey! **Stop!")
        
    def test_non_text_type_nodes(self):
        """This test checks if the function will apend non-TEXT TextType 
            nodes immediately without checking if a delimiter is present."""
        old_nodes = [
                TextNode("START HERE", TextType.BOLD),
                TextNode("This _word_ is _italized_", TextType.TEXT)
                ]
        result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("START HERE", TextType.BOLD),
            TextNode("This ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
            TextNode(" is ", TextType.TEXT),
            TextNode("italized", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        """Tests a TextType.TEXT node with empty text."""
        node = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_input_list(self):
        """Tests an empty list of nodes."""
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        expected = []
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        """Tests a TextType.TEXT node with no delimiter."""
        node = [TextNode("Plain text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)