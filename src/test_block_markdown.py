import unittest
from block_markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_with_many_lines_to_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_with_whitespaces_to_blocks(self):
        md = """
This is **bolded** paragraph

   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line   

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestNumberBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "Just a normal sentece"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        block = "# Just a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_block_to_block_type_heading_2(self):
        block = "###### Just a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_invalid_heading(self):
        block = "###Just a wrong heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_heading_2(self):
        block = "######## Just a wrong heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nJust some code```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_invalid_code(self):
        block = "````Just some code```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_quotes(self):
        block = "> This is a quote\n" + "> This is a second quote\n" + "> This is the last quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_invalid_quote(self):
        block = "> This is a quote\n" + "This is (not) a second quote\n" + "> This is the last quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is an item of an unordered list\n" + "- This is the second item of an unordered list\n" +"- This is the last item of an unordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_list(self):
        block = "- This is an item of an invalid unordered list\n" + "This is the second item of an invalid unordered list\n" + "- This is the last item of an invalid unordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block =  "1. This is an item of a ordered list\n"+ "2. This is the second item of a ordered list\n" + "3. This is the last item of a ordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list(self):
        block = "1. This is an item of an invalid ordered list\n" + "This is the second item of an invalid ordered list\n" + "3. This is the last item of an invalid ordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)                  

class TestBlockNodeToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_heading(self):
        md = """
#### This is a heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h4>This is a heading</h4></div>",
    )

    def test_quotes(self):
        md = """
>This is the first quote without an space 
>This is the same 
> This one has an space
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is the first quote without an space This is the same This one has an space</blockquote></div>",
    )

    def test_unordered_list(self):
        md = """
- This is an item
- This is an item
- This is an item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>This is an item</li><li>This is an item</li><li>This is an item</li></ul></div>",
    )

    def test_ordered_list(self):
        md = """
1. This is item one
2. This is item two
3. This is item three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>This is item one</li><li>This is item two</li><li>This is item three</li></ol></div>",
    )