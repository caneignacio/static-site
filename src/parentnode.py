from htmlnode import HTMLNode
from leafnode import LeafNode

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


