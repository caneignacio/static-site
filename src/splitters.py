# Text Splitters

import re
from enum import Enum
from nodes import ParentNode, LeafNode, TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:

        first_plain_node = 0

        if node.text[:len(delimiter)] == delimiter:
            first_plain_node = 1
            node.text = node.text[len(delimiter):]
        
        if node.text[-len(delimiter):] == delimiter:
            node.text = node.text[0:-len(delimiter)]
        
        split_texts = node.text.split(delimiter)
        split_length = len(split_texts)
        split_nodes = []

        for text in split_texts:
            new = TextNode(text, text_type)
            split_nodes.append(new)
        for i in range(first_plain_node, split_length, 2):
            split_nodes[i].text_type = TextType.TEXT
        for node in split_nodes:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall("!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall("\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(orig_node):
    node = orig_node[0]
    new_nodes = []
    first_empty = False
    if re.search("^!\[(.*?)\]\((.*?)\)", node.text) != None:
        first_empty = True
    new_texts = re.split("!\[(.*?)\]\((.*?)\)", node.text, 1)
    if not first_empty:
        new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
    new_texts = new_texts[1:]
    if len(new_texts) > 1:
        new_nodes.append(TextNode(new_texts[0], TextType.IMAGE, new_texts[1]))
        new_texts = new_texts[2:]
    while len(new_texts) > 0 and new_texts[0] != "":
        first_empty = False
        if re.search("^!\[(.*?)\]\((.*?)\)", new_texts[0]) != None:
            first_empty = True
        new_texts = re.split("!\[(.*?)\]\((.*?)\)", new_texts[0], 1)
        if not first_empty:
            new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
        new_texts = new_texts[1:]
        if len(new_texts) > 1:
            new_nodes.append(TextNode(new_texts[0], TextType.IMAGE, new_texts[1]))
            new_texts = new_texts[2:]
    return new_nodes


def split_nodes_link(orig_node):
    node = orig_node[0]
    new_nodes = []
    first_empty = False
    if re.search("^\[(.*?)\]\((.*?)\)", node.text) != None:
        first_empty = True
    new_texts = re.split("(?<!!)\[(.*?)\]\((.*?)\)", node.text, 1)
    if not first_empty:
        new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
    new_texts = new_texts[1:]
    if len(new_texts) > 1:
        new_nodes.append(TextNode(new_texts[0], TextType.LINK, new_texts[1]))
        new_texts = new_texts[2:]
    while len(new_texts) > 0 and new_texts[0] != "":
        first_empty = False
        if re.search("^\[(.*?)\]\((.*?)\)", new_texts[0]) != None:
            first_empty = True
        new_texts = re.split("(?<!!)\[(.*?)\]\((.*?)\)", new_texts[0], 1)
        if not first_empty:
            new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
        new_texts = new_texts[1:]
        if len(new_texts) > 1:
            new_nodes.append(TextNode(new_texts[0], TextType.LINK, new_texts[1]))
            new_texts = new_texts[2:]
    return new_nodes

def text_to_textnode(text):
    text_nodes_list = [TextNode(text, TextType.TEXT)]

    bold_nodes_list = split_nodes_delimiter(text_nodes_list, "**", TextType.BOLD)
    
    it_nodes_list = []
    for bold in bold_nodes_list:
        if bold.text_type == TextType.TEXT:
            split_italic = split_nodes_delimiter([bold], "_", TextType.ITALIC)
            for it in split_italic:
                it_nodes_list.append(it)
        else:
            it_nodes_list.append(bold)
    
    code_nodes_list = []
    for it in it_nodes_list:
        if it.text_type == TextType.TEXT:
            split_code = split_nodes_delimiter([it], "`", TextType.CODE)
            for code in split_code:
                code_nodes_list.append(code)
        else:
            code_nodes_list.append(it)
    
    link_nodes_list = []
    for code in code_nodes_list:
        if code.text_type == TextType.TEXT:
            split_links = split_nodes_link([code])
            for link in split_links:
                link_nodes_list.append(link)
        else:
            link_nodes_list.append(code)

    image_nodes_list = []
    for link in link_nodes_list:
        if link.text_type == TextType.TEXT:
            split_images = split_nodes_image([link])
            for im in split_images:
                image_nodes_list.append(im)
        else:
            image_nodes_list.append(link)
    
    return image_nodes_list

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception
    

# Block Splitters

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    text_list = markdown.split("\n\n")
    new_list = []
    for text in text_list:
        clean = text.strip()
        if clean != "":
            new_list.append(text.strip("\n "))
    return new_list

def is_code(text):
    if len(text) >= 6 and text[:3] == "```" and text[-3:] == "```":
        return True
    else:
        return False

def is_quote(text):
    quote = True
    lines_list = text.split("\n")
    for line in lines_list:
        if line == "" or line[0] != ">":
            quote = False
    return quote

def is_unordered(text):
    unordered = True
    lines_list = text.split("\n")
    for line in lines_list:
        if line == "" or line[0:2] != f"- ":
            unordered = False
    return unordered

def is_ordered(text):
    ordered = True
    lines_list = text.split("\n")
    i = 0
    while i < len(lines_list):
        char = str(i+1)
        if lines_list[i] == "" or lines_list[i][0:3] != f"{char}. ":
            ordered = False
        i += 1
    return ordered


def strip_bullets(text, char):
    lines_list = text.split("\n")
    for line in lines_list:
        if line != "":
            line = line[char:]
    return "\n".join(lines_list)


def block_to_blocktype(block):
    if re.search("^#{1,6}", block) != None:
        block_type = BlockType.HEADING
    elif is_code(block):
        block_type = BlockType.CODE
    elif is_ordered(block):
        block_type = BlockType.ORDERED_LIST
    elif is_quote(block):
        block_type = BlockType.QUOTE
    elif is_unordered(block):
        block_type = BlockType.UNORDERED_LIST
    else:
        block_type = BlockType.PARAGRAPH
    return block_type

def heading_count(block, block_type):
    if block_type == BlockType.HEADING:
        count = 0
        i = 0
        char = block[i]
        while char == "#":
            count += 1
            i += 1
            char = block[i]
        return count
    else:
        raise ValueError("invalid block type")            

def blocktype_to_html_tag(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return f"h{heading_count(block, block_type)}"
        case BlockType.CODE:
            return "pre><code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        
        case _:
            raise Exception("invalid input")
    

def text_to_children(text):
    text_nodes_list = text_to_textnode(text)
    html_nodes_list = []
    for node in text_nodes_list:
        html_node = text_node_to_html_node(node)
        html_nodes_list.append(html_node)
    return html_nodes_list

def cleaner(text, text_type):
    if text_type == BlockType.ORDERED_LIST:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = "<li>" + l[3:] + "</li>"
                ls.append(l)
        return ("").join(ls)
    elif text_type == BlockType.UNORDERED_LIST:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = "<li>" + l[2:] + "</li>"
                ls.append(l)
        return ("").join(ls)
    elif text_type == BlockType.QUOTE:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = l[1:].strip()
                ls.append(l)
        return (" ").join(ls)
    elif text_type == BlockType.HEADING:
        return text[heading_count(text, text_type):].strip()
    else:
        return text.replace("\n", " ")



def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children_list = []
    for block in block_list:
        block_type = block_to_blocktype(block)
        clean_block = cleaner(block, block_type)
        if block_type == BlockType.CODE:
            block_html_node = LeafNode(blocktype_to_html_tag(block, block_type), block[3:-3].lstrip())
        else:
            block_html_node = ParentNode(blocktype_to_html_tag(block, block_type), text_to_children(clean_block))
        children_list.append(block_html_node)
    return ParentNode("div", children_list)