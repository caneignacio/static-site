import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class LeafTestNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google", {"href": "https//www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https//www.google.com">Google</a>')

    def test_eq_a(self):
        node = LeafNode("a", "Google", {"href": "https//www.google.com"})
        node2 = LeafNode("a", "Google", {"href": "https//www.google.com"})
        self.assertEqual(node, node2)

    def test_noneq_p(self):
        node = LeafNode(None, "Google")
        node2 = LeafNode("a", "Google")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_2(self):
        node = TextNode("Google", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")

    def test_text_3(self):
        node = TextNode("Image", TextType.IMAGE, "www.google.com/image1")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.google.com/image1")
        self.assertEqual(html_node.props["alt"], "Image")

if __name__ == "__main__":
    unittest.main()
