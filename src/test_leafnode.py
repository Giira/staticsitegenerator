import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(value="Print here", tag="a", props={"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Print here</a>', node.to_html())

    def test_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")