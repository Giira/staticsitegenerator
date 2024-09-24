import unittest
from textnode import Textnode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = Textnode("This is a text node", "bold")
        node2 = Textnode("This is a text node", "bold")
        self.assertEqual(node, node2)


    def test_eq_false(self):
        node = Textnode("This", "bold")
        node2 = Textnode("this", "bold")
        self.assertNotEqual(node, node2)

    
    def test_eq_false2(self):
        node = Textnode("This", "bold")
        node2 = Textnode("This", "italic")
        self.assertNotEqual(node, node2)


    def test_eq_url(self):
        node = Textnode("This is a text node", "bold", "http://localhost:8888")
        node2 = Textnode("This is a text node", "bold", "http://localhost:8888")
        self.assertEqual(node, node2)

    
    def test_repr(self):
        node = Textnode("This is a text node", "bold", "http://localhost:8888")
        self.assertEqual(f"TextNode(This is a text node, bold, http://localhost:8888)", repr(node))



if __name__ == "__main__":
    unittest.main()
