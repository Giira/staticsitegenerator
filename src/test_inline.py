import unittest
from textnode import (TextNode, text_type_text, text_type_bold, 
                      text_type_italic, text_type_code )
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


class TestExtractMarkdown(unittest.TestCase):
    def test_markdown_image_eq(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) "
        self.assertEqual(extract_markdown_images(text), 
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_markdown_link_eq(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
                         extract_markdown_links(text))
        
    def test_link_avoid_image(self):
        text = "This is text ![img text](img src) and so is this [link text](link address)"
        self.assertEqual(extract_markdown_links(text), 
                         [("link text", "link address")])