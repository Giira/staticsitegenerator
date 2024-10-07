from textnode import (TextNode, text_type_text)

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
                    new_nodes.append(TextNode(segment, text_type, node.url))
                    type_counter = 0

    return new_nodes    
