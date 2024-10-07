import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(value="Print here", tag="a", props={"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Print here</a>', node.to_html())

    def test_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")


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


if __name__ == "__main__":
    unittest.main()
