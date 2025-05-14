import unittest

from textnode import TextNode, TextType

class testtextnode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("sample text", TextType.BOLD, "www.fakewebsite.com")
        node2 = TextNode("sample text", TextType.BOLD, "www.anothersite.com")
        self.assertNotEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("sample text", TextType.BOLD)
        node2 = TextNode("different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()