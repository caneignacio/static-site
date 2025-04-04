import unittest

from textnode import TextType, TextNode
import leafnode
import htmlnode
import parentnode
from splitters import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode

class Splitters(unittest.TestCase):
    def test_equal(self):
        old_nodes = [TextNode("This is a node without bolds.", TextType.TEXT), TextNode("This is another with a **bold** word.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), [TextNode("This is a node without bolds.", TextType.TEXT), TextNode("This is another with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word.", TextType.TEXT)])
                             
    def test_equal_2(self):
        node = [TextNode("This is a test with a **bold** and an _italic_ word.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), [TextNode("This is a test with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" and an _italic_ word.", TextType.TEXT)])
    
    def test_equal_3(self):
        node = [TextNode("_This_ text begins with _italic._", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "_", TextType.ITALIC), [TextNode("This", TextType.ITALIC), TextNode(" text begins with ", TextType.TEXT), TextNode("italic.", TextType.ITALIC)])
    
    def test_equal_4(self):
        node = [TextNode("_This_ text does not end in italic.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "_", TextType.ITALIC), [TextNode("This", TextType.ITALIC), TextNode(" text does not end in italic.", TextType.TEXT)])
    
    def test_equal_5(self):
        node = [TextNode("This text has no formats.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), [TextNode("This text has no formats.", TextType.TEXT)])

    def test_equal_6(self):
        old_nodes = [TextNode("This is a node with **bold.**", TextType.TEXT), TextNode("This is another with a **bold.**", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), [TextNode("This is a node with ", TextType.TEXT), TextNode("bold.", TextType.BOLD), TextNode("This is another with a ", TextType.TEXT), TextNode("bold.", TextType.BOLD)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.google.com)")
        self.assertListEqual([("link", "https://www.google.com")], matches)
    
    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images("![new_image](https://image.png)")
        self.assertEqual([("new_image", "https://image.png")], matches)
    
    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links("This is a text with one [link](https://www.wikipedia.org) and also [another_link](https://www.google.com)")
        self.assertEqual([("link", "https://www.wikipedia.org"), ("another_link", "https://www.google.com")], matches)
    
    def test_split_images_1(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_2(self):
        node = TextNode("This is an ![image](https://i.imgur.com/abcd.png) but this is [not](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/abcd.png"), TextNode(" but this is [not](https://google.com)", TextType.TEXT)], new_nodes)
    

    def test_split_links_1(self):
        node = TextNode("This is an ![image](https://i.imgur.com/abcd.png) but this is [not](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is an ![image](https://i.imgur.com/abcd.png) but this is ", TextType.TEXT), TextNode("not", TextType.LINK,"https://google.com")], new_nodes)
    

    def test_split_links_2(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is a plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is a plain text", TextType.TEXT)], new_nodes)
    

    def test_split_no_links(self):
        node = TextNode("This is a plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is a plain text", TextType.TEXT)], new_nodes)
    

    def test_starts_and_ends_with_image(self):
        node = TextNode("![image](https://image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://image.png")], new_nodes)


    def test_starts_and_ends_with_link(self):
        node = TextNode("[link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://www.google.com")], new_nodes)
    

    def test_full_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual([TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")], new_nodes)
    
    def test_full_text_to_textnode_2(self):
        text = "**text**_italic_`code block`![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual([TextNode("text", TextType.BOLD), TextNode("italic", TextType.ITALIC), TextNode("code block", TextType.CODE), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode("link", TextType.LINK, "https://boot.dev")], new_nodes)
    
    def test_plain_text_to_textnode(self):
        text = "Hello World!"
        new_nodes = text_to_textnode(text)
        self.assertListEqual([TextNode("Hello World!", TextType.TEXT)], new_nodes)