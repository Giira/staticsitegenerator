import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_eq(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ], )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_th_props_eq(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ], 
        {"href": "www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<p href="www.google.com" target="_blank"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_leaf_props(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text", {"href": "www.google.com"}),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ], )
        self.assertEqual(node.to_html(), '<p><b href="www.google.com">Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_single_child(self):
        node = ParentNode("h2", [LeafNode("b", "child")])
        self.assertEqual(node.to_html(), "<h2><b>child</b></h2>")

    def test_grandchild(self):
        grandnode = LeafNode("span", "grandchild")
        childnode = ParentNode("i", [grandnode])
        node = ParentNode("h3", [childnode])
        self.assertEqual(node.to_html(), '<h3><i><span>grandchild</span></i></h3>')