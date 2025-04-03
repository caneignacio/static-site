import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class ParentTestNode(unittest.TestCase):
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

    def test_to_html_with_empty_children(self):
        child_node = None
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_empty_grandchildren(self):
        grandchild_node = None
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span></span></div>")

    def test_to_html_with_n_great_grandchildren(self):
        great_great_grandchild_node = LeafNode("i", "great_great_grandchild")
        great_grandchild_node_1 = ParentNode("span", [great_great_grandchild_node])
        great_grandchild_node_2 = LeafNode("a", "Google", {"href": "https://www.google.com"})
        grandchild_node = ParentNode("div", [great_grandchild_node_1, great_grandchild_node_2])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><div><span><i>great_great_grandchild</i></span><a href="https://www.google.com">Google</a></div></span></div>')

if __name__ == "__main__":
    unittest.main()
