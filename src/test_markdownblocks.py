import unittest
from markdownblocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_eq(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertEqual(markdown_to_blocks(markdown), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ])

    def test_extra_chars(self):
        markdown = """
# Heading



Paragraph   

*List 1
*List 2
*List 3 
"""
        self.assertEqual(markdown_to_blocks(markdown), [
            "# Heading",
            "Paragraph",
            "*List 1\n*List 2\n*List 3"
        ])