import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    
    def test_eq_repr(self):
        node = HTMLNode("h1", "test", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(h1, test, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))


    def test_eq_None(self):
        node = HTMLNode(tag="h2")
        self.assertEqual(None, node.value)