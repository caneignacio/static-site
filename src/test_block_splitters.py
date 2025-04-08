import unittest

from splitters import BlockType, markdown_to_blocks, block_to_blocktype, markdown_to_html_node



class BlockSplittersTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is a line with some trailling whitespaces   


This is another paragraph and it has two lines.
The second line leaves a few extra jumps




- This is a list with a unique element
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a line with some trailling whitespaces", "This is another paragraph and it has two lines.\nThe second line leaves a few extra jumps", "- This is a list with a unique element"])


    def test_empty_text(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    
    def test_empty_lines(self):
        st = """



"""
        blocks = markdown_to_blocks(st)
        self.assertEqual(blocks, [])


    def test_blocktypes1(self):
        st = "### This is a heading"
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.HEADING)
    
    def test_blocktypes2(self):
        st = "```This is code```"
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.CODE)
    
    def test_blocktypes3(self):
        st = """> This is a quote block
> That extends through
> More than one line."""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.QUOTE)
    
    def test_blocktypes4(self):
        st = """- This is a list
- Which is not ordered"""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
    
    def test_blocktypes5(self):
        st = """1. This is a list
2. Which is ordered"""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
    
    def test_blocktypes6(self):
        st = """1. This is a list
2. Which is ordered
4. But there's a problem
3. With the numbers
5. So it should be a plain paragraph"""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)


    def test_blocktypes7(self):
        st = """1. This is an ordered list

2. With a similar problem"""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)


    def test_blocktypes8(self):
        st = "1. This is an ordered list with only one element."
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
    
    def test_blocktypes9(self):
        st = """```
This is code that extends through some
lines

```"""
        blocktype = block_to_blocktype(st)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )


    def test_heading(self):
        md = """
###This is a heading


Then followed by a paragraph
with _italic_ text and **bold**

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><h3>This is a heading</h3><p>Then followed by a paragraph with <i>italic</i> text and <b>bold</b></p></div>",
    )


    def test_heading_and_ordered(self):
        md = """
###This is a heading


1. Then followed by a list
2. Which is _ordered_
3. Though it has some linefeeds



"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><h3>This is a heading</h3><ol><li>Then followed by a list</li><li>Which is <i>ordered</i></li><li>Though it has some linefeeds</li></ol></div>",
    )


    def test_unordered_and_quotes(self):
        md = """
>This is a very
>famous quote

The quote is by a well-known author

These are other books he wrote:

- Book one
- Book two
- Book three



"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><blockquote>This is a very famous quote</blockquote><p>The quote is by a well-known author</p><p>These are other books he wrote:</p><ul><li>Book one</li><li>Book two</li><li>Book three</li></ul>bootdev run 1d9f9063-4163-4b0e-ba00-397f7e7d37b9 -s</div>"
    )


if __name__ == "__main__":
    unittest.main()