import re
from textnode import (TextNode, text_type_text, text_type_image, text_type_link, 
text_type_bold, text_type_italic, text_type_code)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            type_counter = 0
            for segment in split_node:
                if segment == "":
                    type_counter = 1
                    continue
                if type_counter == 0:
                    new_nodes.append(TextNode(segment, node.text_type))
                    type_counter = 1
                else:
                    new_nodes.append(TextNode(segment, text_type))
                    type_counter = 0

    return new_nodes    


def extract_markdown_images(text):
    images = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return images


def extract_markdown_links(text):
    links = re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images is None:
            new_nodes.append(node)
        else:
            segments = re.split(r'!\[(.*?)\]\((.*?)\)', node.text)
            type_counter = 0
            image_counter = 0
            for segment in segments:
                if segment == "":
                    type_counter = 1
                    continue
                if type_counter == 0:
                    new_nodes.append(TextNode(segment, text_type_text))
                    type_counter = 1
                elif type_counter == 1:
                    new_nodes.append(TextNode(images[image_counter][0], text_type_image, images[image_counter][1]))
                    image_counter += 1
                    type_counter = 2
                else:
                    type_counter = 0
                    continue
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links is None:
            new_nodes.append(node)
        else:
            segments = re.split(r'(?<!!)\[(.*?)\]\((.*?)\)', node.text)
            type_counter = 0
            link_counter = 0
            for segment in segments:
                if segment == "":
                    type_counter = 1
                    continue
                if type_counter == 0:
                    new_nodes.append(TextNode(segment, text_type_text))
                    type_counter = 1
                elif type_counter == 1:
                    new_nodes.append(TextNode(links[link_counter][0], text_type_link, links[link_counter][1]))
                    link_counter += 1
                    type_counter = 2
                else:
                    type_counter = 0
                    continue
    return new_nodes


def text_to_textnodes(text):
    start = [TextNode(text, text_type_text)]
    minus_bold = split_nodes_delimiter(start, "**", text_type_bold)
    minus_italic = split_nodes_delimiter(minus_bold, "*", text_type_italic)
    minus_code = split_nodes_delimiter(minus_italic, "`", text_type_code)
    minus_img = split_nodes_image(minus_code)
    output = split_nodes_link(minus_img)
    return output
