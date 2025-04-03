import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is another test node", TextType.ITALIC, "www.google.com")
        node2 = TextNode("This is another test node", TextType.ITALIC, "www.google.com")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("This is one test node", TextType.ITALIC)
        node2 = TextNode("This is another test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq2(self):
        node = TextNode("This is the last test node", TextType.TEXT, "www.google.com")
        node2 = TextNode("This is the last test node", TextType.TEXT)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
