import unittest

from htmlnode import HTMLNode

node_test_1 = HTMLNode("a")
node_test_2 = HTMLNode()
children_list = [node_test_1, node_test_2]
attributes_dict = {"contenteditable": "false"}

class HTMLTestNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = HTMLNode("p", "This is a paragraph", children_list, attributes_dict)
        node2 = HTMLNode("p", "This is a paragraph", children_list, attributes_dict)
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("a")
        self.assertNotEqual(node, node2)

    def test_noneq_2(self):
        node = HTMLNode("p", "This is a paragraph", children_list)
        node2 = HTMLNode("p", "This is a paragraph", children_list, attributes_dict)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
