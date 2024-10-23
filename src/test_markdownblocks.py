import unittest
from htmlnode import ParentNode, LeafNode
from markdownblocks import (markdown_to_blocks, block_to_block_type, block_type_to_tag, 
                            lists_to_children, typed_parent_node, markdown_to_html_node)

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

    def test_block_to_tag(self):
        block = "### block"
        self.assertEqual(block_type_to_tag("heading", block), "h3")


class TestListsToChildren(unittest.TestCase):
    def test_eq(self):
        list = "1. line1\n2. line2\n3. line3"
        block_type = "ordered_list"
        self.assertEqual(lists_to_children(list, block_type), [
            ParentNode("li", [LeafNode(None, "line1")]),
            ParentNode("li", [LeafNode(None, "line2")]),
            ParentNode("li", [LeafNode(None, "line3")])
            ])
        
    def test_eq_2(self):
        list = "1. **line1**\n2. line2\n3. line3"
        block_type = "ordered_list"
        self.assertEqual(lists_to_children(list, block_type), [
            ParentNode("li", [LeafNode("b", "line1")]),
            ParentNode("li", [LeafNode(None, "line2")]),
            ParentNode("li", [LeafNode(None, "line3")])
            ])
        
    def test_eq_3(self):
        list = "1. **line1** secret text\n2. line2\n3. line3"
        block_type = "ordered_list"
        self.assertEqual(lists_to_children(list, block_type), [
            ParentNode("li", [LeafNode("b", "line1"), LeafNode(None, " secret text")]),
            ParentNode("li", [LeafNode(None, "line2")]),
            ParentNode("li", [LeafNode(None, "line3")])
            ])


class TestTypedParentNode(unittest.TestCase):
    def test_eq(self):
        block = "some **text** and `code`"
        typed_block = (block, "paragraph")
        self.assertEqual(typed_parent_node(typed_block), ParentNode("p", [
            LeafNode(None, "some "),
            LeafNode("b", "text"),
            LeafNode(None, " and "),
            LeafNode("code", "code")
        ]))


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_eq(self):
        markdown = """# This is a heading

>This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another **list** item"""

        self.assertEqual(markdown_to_html_node(markdown), ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "This is a heading")]),
            ParentNode("blockquote", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it.")
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "This is the first list item in a list block")]),
                ParentNode("li", [LeafNode(None, "This is a list item")]),
                ParentNode("li", [
                    LeafNode(None, "This is another "),
                    LeafNode("b", "list"),
                    LeafNode(None, " item")
                ])
            ])
        ]))