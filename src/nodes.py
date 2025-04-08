#HTML Node
from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        to_html = ""
        for prop in self.props.keys():
            to_html += f' {prop}="{self.props[prop]}"'
        return to_html

    def __repr__(self):
        print(f"TAG: {self.tag}")
        print(f"VALUE: {self.value}")
        print(f"CHILDREN: {self.children}")
        print(f"PROPS: {self.props}")

# Parent Node

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        html_text = ""
        if self.tag == None:
            raise ValueError("tag missing")
        elif self.children == None:
            raise ValueError("children missing")
        else:
            html_text += f"<{self.tag}>"
            for child in self.children:
                if isinstance(child, HTMLNode):
                    html_text += f"{child.to_html()}"
            html_text += f"</{self.tag}>"
            return html_text


# Leaf Node

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return str(self.value)
        elif self.props == None:
            if self.tag == "pre><code":
                return f"<{self.tag}>{self.value}</code></pre>"
            else:    
                return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            if self.tag == "pre><code":
                return f"<{self.tag}{self.props_to_html()}>{self.value}</code></pre>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



#Text Node

class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "__Italic text__"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
