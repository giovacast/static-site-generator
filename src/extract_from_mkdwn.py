import re

def extract_markdown_images(text):
    """Takes markdown text and returns a list of tuples. Each tuple contains
        the alt text and the URL of any markdown images."""
    if not isinstance(text, str):
        raise TypeError("Markdown text must be a string.")
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    """Extracts markdown links and returns tuples of anchor text and URLs."""
    if not isinstance(text, str):
        raise TypeError("Markdown text must be a string.")
    links = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)  # Excludes ![text](url)
    return links