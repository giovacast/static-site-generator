from textnode import TextNode, TextType

def main():
    # Create a TextNode object with dummy values
    node = TextNode("Sample text", TextType.LINK, "https://example.com")
    # Print the object using repr to show its details
    print(node.__repr__())

if __name__ == "__main__":
    main()