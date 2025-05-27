import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from node_converter import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Click here!", TextType.LINK, "www.website.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here!")
        self.assertEqual(html_node.props, {"href": "www.website.com"})

    def test_img(self):
        node = TextNode("Image of an orange", TextType.IMAGE, 
                        "/shared-assets/images/examples/orange.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, 
                         {"src": "/shared-assets/images/examples/orange.jpg",
                          "alt": "Image of an orange"})
        
    def test_text_is_none(self):
        node = TextNode(None, TextType.BOLD, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_wrong_text_type(self):
        node = TextNode("Hello", TextType.TEXT, None)
        node.text_type = "INVALID"
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Invalid TextType: INVALID")

    def test_bold(self):
        node = TextNode("STOP", TextType.BOLD, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "STOP")