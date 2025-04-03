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
