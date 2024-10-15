import unittest
from markdownblocks import markdown_to_blocks, block_to_block_type

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


class TestBlockToBlockType(unittest.TestCase):
    def test_eq_heading(self):
        block = "###### block"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_eq_heading2(self):
        block = "####### block"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_eq_heading3(self):
        block = "###block"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_eq_code(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_eq_code2(self):
        block = "```code``"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_eq_code_3(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_eq_code4(self):
        block = "``` ```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_eq_quote(self):
        block = ">line\n>line2\n>line3"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_eq_quote2(self):
        block = ">line\nline2"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_one_quote(self):
        block = ">quote"
        self.assertEqual(block_to_block_type(block), "quote")
    
    def test_eq_unordered_list(self):
        block = "* 1\n* 2\n* 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_eq_unordered_list2(self):
        block = "* 1\n- 2\n* 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")
    
    def test_eq_unordered_list3(self):
        block = "* 1\n*2\n* 3"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_eq_ordered_list(self):
        block = "1. line\n2. line\n3. line"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_eq_ordered_list2(self):
        block = "1. line\n4. line\n3. line"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_eq_ordered_list2(self):
        block = "1. line\n2. line\n3.line"
        self.assertEqual(block_to_block_type(block), "paragraph")