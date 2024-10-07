import unittest
from textnode import (TextNode, text_type_text, text_type_bold, 
                      text_type_italic, text_type_code)
from inline import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ])

    def test_double_segment(self):
        node = TextNode("This `is` text with a `code block` word", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), [
            TextNode("This ", text_type_text),
            TextNode("is", text_type_code),
            TextNode(" text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ])

    def test_double_asterisk(self):
        node = TextNode("This is some **bold** text", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "**", text_type_bold), [
            TextNode("This is some ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ])

    def test_multiple_nodes(self):
        node1 = TextNode("Hi *italic* words", text_type_text)
        node2 = TextNode("Bye *italic* words", text_type_text)
        self.assertEqual(split_nodes_delimiter([node1, node2], "*", text_type_italic), [
            TextNode("Hi ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" words", text_type_text),
            TextNode("Bye ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" words", text_type_text)
        ])

    def test_non_text(self):
        node1 = TextNode("Hi", text_type_bold)
        node2 = TextNode("Bye *italic*", text_type_text)
        self.assertEqual(split_nodes_delimiter([node1, node2], "*", text_type_italic), [
            TextNode("Hi", text_type_bold),
            TextNode("Bye ", text_type_text),
            TextNode("italic", text_type_italic)
        ])

    def test_two_delimiters(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes  = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(split_nodes_delimiter(new_nodes, "*", text_type_italic), [
            TextNode("bold", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("italic", text_type_italic)
        ])