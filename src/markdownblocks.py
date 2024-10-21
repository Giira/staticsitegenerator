from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode
from inline import text_to_textnodes

def markdown_to_blocks(markdown):
    text_list = [item.strip() for item in markdown.split("\n\n")]
    output_list = []
    for item in text_list:
        if item != "":
            output_list.append(item)
    return output_list


def block_to_block_type(block):
    line_list = block.split("\n")
    if block[0] == "#":
        hash_counter = 0
        for letter in block:
            if letter == "#":
                hash_counter += 1
                if hash_counter > 6:
                    return "paragraph"
                else:
                    continue
            if letter != " ":
                return "paragraph"
            elif letter == " ":
                return "heading"
    elif block[0:3] == "```" and len(block) >6 and block[-3:] == "```":
        return "code"
    elif block[0] == ">":
        for line in line_list:
            if line[0] != ">":
                return "paragraph"
        return "quote"
    elif block[0:2] == "* " or block[0:2] == "- ":
        for line in line_list:
            if line[:2] != "* " and line[:2] != "- ":
                return "paragraph"
        return "unordered_list"
    elif block[0].isnumeric() and block[1:3] == ". ":
        counter = 1
        for line in line_list:
            if int(line[0]) != counter or line[1:3] != ". ":
                return "paragraph"
            counter += 1
        return "ordered_list"
    else:
        return "paragraph"
    

def block_type_to_tag(block_type, block):
    if block_type == "paragraph":
        return "p"
    if block_type == "heading":
        hash_count = 0
        for character in block:
            if character == "#":
                hash_count += 1
            else:
                return f"h{hash_count}"
    if block_type == "code":
        return "code"
    if block_type == "quote":
        return "q"
    if block_type == "unordered_list":
        return "ul"
    if block_type == "ordered_list":
        return "ol"
    else:
        raise ValueError(f"'{block_type}' is an invalid block type")
    

def text_to_children(text):
    nodes = text_to_textnodes(text)
    leaves = []
    for node in nodes:
        leaves.append(text_node_to_html_node(node))
    return leaves


def lists_to_children(text, block_type):
    if block_type == "ordered_list":
        lines2 = text.split("\n")
        lines = []
        for line in lines2:
            space_count = 1
            kill = False
            for character in line:
                if not kill:
                    if character != " ":
                        space_count += 1
                    else:
                        lines.append(line[space_count:])
                        kill = True
                else:
                    continue

    if block_type == "unordered_list":
        lines = [line.lstrip("* ") for line in text.split("\n")]

    children = []
    for line in lines:
        leaves = text_to_children(line)
        children.append(ParentNode("li", leaves))
    return children


def typed_parent_node(typed_block):
    tag = block_type_to_tag(typed_block[1], typed_block[0])
    
    if tag == "p":
        text = typed_block[0]
        children = text_to_children(text)
    elif tag[0] == "h":
        text = typed_block[0][int(tag[1]) + 1:]
        children = text_to_children(text)
    elif tag == "code":
        text = typed_block[0][3:]
        children = text_to_children(text)
    elif tag == "q":
        text = typed_block[0].lstrip(">")
        children = text_to_children(text)
    else:
        children = lists_to_children(typed_block[0], typed_block[1])

    return ParentNode(tag, children)

    
def markdown_to_html_node(markdown):
    children = []
    typed_blocks = []
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        typed_blocks.append((block, block_to_block_type(block)))
    for typed_block in typed_blocks:
        children.append(typed_parent_node(typed_block))

    return ParentNode("div", children)
