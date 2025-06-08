import unittest
from extract_from_mkdwn import extract_markdown_images, extract_markdown_links

class TestExtractFromMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        """Tests whether the function can extract the alt text and URL of
            the image."""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        """Tests whether the fuinction can extract the anchor test and URL 
            of each link."""
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), 
                    ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)

    def test_text_not_string(self):
        """Test the type of the argument passed to the function which should 
            be a string."""
        with self.assertRaises(TypeError) as e:
            extract_markdown_images([1])
        self.assertEqual(str(e.exception), "Markdown text must be a string.")

    def test_mixed_images_and_links(self):
        """Tests that images and links are extracted correctly from mixed content."""
        text = ("This is an ![image](https://i.imgur.com/zjjcJKZ.png) "
                "and a [link](https://www.boot.dev)")
        # Test images
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        # Test links
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], link_matches)

    def test_no_matches(self):
        """Tests text with no images or links returns an empty list."""
        text = "Plain text with no links or images."
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_empty_string(self):
        """Tests an empty string input returns an empty list."""
        text = ""
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_multiple_images(self):
        """Tests extraction of multiple markdown images."""
        text = ("![img1](https://i.imgur.com/1.png) "
                "and ![img2](https://i.imgur.com/2.png)")
        expected = [
            ("img1", "https://i.imgur.com/1.png"),
            ("img2", "https://i.imgur.com/2.png"),
        ]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_malformed_markdown(self):
        """Tests that incomplete markdown syntax is ignored."""
        text = ("Incomplete [text]( and [text] and ![alt]( and ![alt] "
                "and [text](url")
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_nested_brackets(self):
        """Tests markdown with nested brackets or parentheses."""
        text = "Link [text [nested]](https://example.com/nested)"
        expected = [("text [nested]", "https://example.com/nested")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_whitespace_in_markdown(self):
        """Tests markdown with extra whitespace."""
        text = "Image ![ alt ]( https://i.imgur.com/zjjcJKZ.png )"
        expected = [(" alt ", " https://i.imgur.com/zjjcJKZ.png ")]
        self.assertListEqual(expected, extract_markdown_images(text))