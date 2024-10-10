import unittest
from textnode import (TextNode, text_type_text, text_type_bold, text_type_link, 
                      text_type_italic, text_type_code, text_type_image)
from inline import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, 
                    split_nodes_image, split_nodes_link, text_to_textnodes)

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
        

class TestSplitImages(unittest.TestCase):
    def test_split_image_eq(self):
        text = "This is an image: ![img](www.img), see!"
        node = TextNode(text, text_type_text)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is an image: ", text_type_text),
            TextNode("img", text_type_image, "www.img"),
            TextNode(", see!", text_type_text)
        ])

    def test_two_imgs_eq(self):
        text = "This is an image: ![img](www.img), and this: ![img2](www.img2)"
        node = TextNode(text, text_type_text)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is an image: ", text_type_text),
            TextNode("img", text_type_image, "www.img"),
            TextNode(", and this: ", text_type_text),
            TextNode("img2", text_type_image, "www.img2"),
        ])
    
    def test_no_text(self):
        text = "![img](www.img)![img2](www.img2)"
        node = TextNode(text, text_type_text)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("img", text_type_image, "www.img"),
            TextNode("img2", text_type_image, "www.img2")
        ])

    def test_two_nodes(self):
        text = "This is an image: ![img](www.img), see!"
        node = TextNode(text, text_type_text)
        self.assertEqual(split_nodes_image([node, node]), [
            TextNode("This is an image: ", text_type_text),
            TextNode("img", text_type_image, "www.img"),
            TextNode(", see!", text_type_text),
            TextNode("This is an image: ", text_type_text),
            TextNode("img", text_type_image, "www.img"),
            TextNode(", see!", text_type_text)
        ])

    def test_no_images(self):
        node = TextNode("Hey you!", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("Hey you!", text_type_text)])


class TestSplitLinks(unittest.TestCase):
    def test_split_link_eq(self):
        text = "This is a link: [link](www.link), this isn't: ![img](img)"
        node = TextNode(text, text_type_text)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is a link: ", text_type_text),
            TextNode("link", text_type_link, "www.link"),
            TextNode(", this isn't: ![img](img)", text_type_text)
        ])


class TestTextToTextNodes(unittest.TestCase):
    def test_eq(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ])

    def test_no_text(self):
        text = "**bold text**`code block`*italics*"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("bold text", text_type_bold),
            TextNode("code block", text_type_code),
            TextNode("italics", text_type_italic)
        ])

    def test_bold_into_italics(self):
        text = "**bold***italic* probs not"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("bold", text_type_bold),
            TextNode("italic", text_type_italic),
            TextNode(" probs not", text_type_text)
        ])