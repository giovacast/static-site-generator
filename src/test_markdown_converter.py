import unittest
from textnode import TextType, TextNode
from markdown_to_textnode import split_nodes_delimiter, split_nodes_image
from markdown_to_textnode import split_nodes_link
from text_to_textnodes import text_to_textnodes

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

class TestExtractImagesFromMarkdown(unittest.TestCase):

    def test_split_images(self):
        node = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT),
            TextNode("This is a second TextNode with an ![image]"
                     "(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is a second TextNode with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    def test_non_textnode_passed(self):
        node = ["This is text with an "
                "![image](https://i.imgur.com/zjjcJKZ.png)"]

        with self.assertRaises(TypeError) as e:
            split_nodes_image(node)
        self.assertEqual(str(e.exception), "TypeError: node needs to be "
                         "a TextNode.")
        
    def test_nontext_texttype(self):
        node = [TextNode("image", TextType.IMAGE, 
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is a second TextNode with an ![image]"
                     "(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
                ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, 
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is a second TextNode with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, 
                         "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
    
    def test_no_images(self):
        node = [TextNode("This is only text with no images.", TextType.TEXT)]

        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is only text with no images.", TextType.TEXT)
            ],
            new_nodes
        )

class TestExtractLinksFromMarkdown(unittest.TestCase):

    def test_split_links(self):
        node = [TextNode("This is text with a link "
                        "[to boot dev](https://www.boot.dev) and "
                        "[to youtube](https://www.youtube.com/@bootdotdev)",
                        TextType.TEXT),
                TextNode("This is a second node with a link [to Google]"
                "(https://www.google.com) to see if the function can loop " \
                "over multiple TextNodes", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(node)
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, 
                         "https://www.youtube.com/@bootdotdev"),
                TextNode("This is a second node with a link ", TextType.TEXT),
                TextNode("to Google", TextType.LINK, "https://www.google.com"),
                TextNode(" to see if the function can loop "
                "over multiple TextNodes", TextType.TEXT)
            ],
            new_nodes
        )

    def test_non_textnode_passed(self):
        node = ["This is a link [to YouTube](https://www.youtube.com)"]

        with self.assertRaises(TypeError) as e:
            split_nodes_link(node)
        self.assertEqual(str(e.exception), "TypeError: node needs to be "
                         "a TextNode.")
        
    def test_nontext_texttype(self):
        node = [TextNode("to Google", TextType.LINK, 
                         "https://www.google.com"),
                TextNode("This is a second TextNode with another link "
                "[to YouTube](https://www.youtube.com)." , TextType.TEXT)
                ]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("to Google", TextType.LINK, 
                         "https://www.google.com"),
                TextNode("This is a second TextNode with another link ", 
                         TextType.TEXT),
                TextNode("to YouTube", TextType.LINK, 
                         "https://www.youtube.com"),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_no_links(self):
        node = [TextNode("This is only text with no links.", TextType.TEXT)]

        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is only text with no links.", TextType.TEXT)
            ],
            new_nodes
        )

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):

        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` " \
"and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) " \
"and a [link](https://boot.dev)")
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, 
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
            ]
            , nodes
        )