from textnode import TextNode, TextType
import os
import shutil

def copy_directory_contents(source, destination):
    """Copies all files and subdirectories from within a
    directory to the main destination directory."""
    source_dir = os.listdir(source)
    for item in source_dir:
        full_source_path = os.path.join(source, item)
        full_destination_path = os.path.join(destination, item)
        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_destination_path)
            print(f"Copying file \"{item}\" from {full_source_path} to {full_destination_path}")
        else:
            os.mkdir(full_destination_path, mode=0o755)
            copy_directory_contents(full_source_path, full_destination_path)

def copy_to_directory(source, destination):
    """Copies the entire contents of the source directory
    to a destination directory."""
    # Delete all contents in the destination directory
    # 1. Use the destination address, check if it exists
    # 2. Delete every directory and file in it
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination, mode=0o755)
    else:
        os.mkdir(destination, mode=0o755)

    copy_directory_contents(source, destination)

def main():
    # Create a TextNode object with dummy values
    node = TextNode("Sample text", TextType.LINK, "https://example.com")
    # Print the object using repr to show its details
    source = "/Users/giovannicastiglione/workspace/github.com/giovacast/static-site-generator/static"
    destination = "/Users/giovannicastiglione/workspace/github.com/giovacast/static-site-generator/public"
    copy_to_directory(source, destination)
    print(node.__repr__())

if __name__ == "__main__":
    main()