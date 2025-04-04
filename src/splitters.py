import htmlnode
from textnode import TextNode, TextType
import leafnode
import parentnode
import re

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