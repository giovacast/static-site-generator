import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

children = ["h2", "h3", "p"]

single_prop = {"href": "https://www.google.com"}

props = {
    "href": "https://www.google.com",
    "target": "_blank",
    }


class testhtmlnode(unittest.TestCase):
    def test_props_eq_none(self):
        node = HTMLNode("h1", "Title", children, None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_single_prop(self):
        node = HTMLNode("h1", "Title", children, single_prop)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_mult_props(self):
        node = HTMLNode("h1", "Title", children, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_no_value(self):
        node = LeafNode("p", None, props)
        with self.assertRaises(ValueError):
            node.to_html()

    children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ]
    incorrect_type_children = [
            1,
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ]

    def test_no_tag(self):
        node = ParentNode(None, children)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_children_is_none(self):
        node = ParentNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = ParentNode("h1", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        

if __name__ == "__main__":
    unittest.main()