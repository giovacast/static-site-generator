import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        """Tests that a markdown paragraph is turned to html"""    
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        print(html)

    def test_codeblock(self):
        """Tests that a markdown code block is turned to html"""
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        print(html)

    def test_heading(self):
        """Tests that a markdown heading is turned to html"""
        md = "# This is a heading"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>"
        )

    def test_quoteblock(self):
        """Tests that a markdown quote block is turned to html"""
        md = "> This is a quote block\n"\
        "> It can have a single line\n"\
        "> Or it can have multiple lines\n"\
        "> Like this one"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block It can have a single line Or it can have multiple lines Like this one</blockquote></div>"
        )

    def test_unordered_list(self):
        """Tests that a markdown unordered list is turned to html"""
        md = """
    - Item one
    - Item two with **bold** text
    - Item three
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two with <b>bold</b> text</li><li>Item three</li></ul></div>"
        )
        print(repr(html))
    
    def test_ordered_list(self):
        """Tests that a markdown ordered list is turned to html"""
        md = """
    1. First item
    2. Second item with _italic_ text
    3. Third item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i> text</li><li>Third item</li></ol></div>"
        )
        print(repr(html))