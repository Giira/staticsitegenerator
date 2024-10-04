import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


    def test_eq_false(self):
        node = TextNode("This", "bold")
        node2 = TextNode("this", "bold")
        self.assertNotEqual(node, node2)

    
    def test_eq_false2(self):
        node = TextNode("This", "bold")
        node2 = TextNode("This", "italic")
        self.assertNotEqual(node, node2)


    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8888")
        node2 = TextNode("This is a text node", "bold", "http://localhost:8888")
        self.assertEqual(node, node2)

    
    def test_repr(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8888")
        self.assertEqual(f"TextNode(This is a text node, bold, http://localhost:8888)", repr(node))


    def test_to_html_text(self):
        node = TextNode("hello", "text_type_text")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode(None, "hello")))

    
    def test_to_html_bold(self):
        node = TextNode("hello", "text_type_bold")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode("b", "hello")))

    
    def test_to_html_italic(self):
        node = TextNode("hello", "text_type_italic")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode("i", "hello")))

    
    def test_to_html_code(self):
        node = TextNode("hello", "text_type_code")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode("code", "hello")))


    def test_to_html_link(self):
        node = TextNode("hello", "text_type_link", "www.google.com")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode("a", "hello", {"href": "www.google.com"})))

    
    def test_to_html_italic(self):
        node = TextNode("hello", "text_type_image", "www.google.com")
        self.assertEqual(repr(text_node_to_html_node(node)), repr(LeafNode("img", "", {"src": "www.google.com", "alt": "hello"})))


if __name__ == "__main__":
    unittest.main()
