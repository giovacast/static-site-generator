class HTMLNode:
    """Represents a 'node' in an HTML document tree 
    (like a <p> tag and its contents, or an <a> tag and its contents). 
    It can be block level or inline, and is designed to only output HTML"""
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):        
        if self.props is None:
            return ""

        html_attributes = ""
        for k, v in self.props.items():
            html_attributes += f' {k}="{v}"'
        return html_attributes
    
    def __repr__(self):
        return f"HTML Node({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    """This class represents a type of HTMLNode that represents 
    a single HTML tag with no children."""

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    """This class will handle the nesting of HTML nodes inside of one another. 
    Any HTML node that's not "leaf" node (i.e. it has children) 
    is a "parent" node"""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        children = ""
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML parent node: children is None")
        if self.children == []:
            raise ValueError("invalid HTML parent node: children list is empty")
        if not all(isinstance(item, HTMLNode) for item in self.children):
            raise TypeError("All children must be HTMLNode instances")
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"            
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"