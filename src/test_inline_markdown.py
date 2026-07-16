import unittest
from textnode import TextNode, TextType
from inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This is a *bold* text", TextType.PLAIN)]
        delimiter = "*"
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.PLAIN))

    def test_split_nodes_delimiter_odd(self):
        old_nodes = [TextNode("This is a *bold* text*", TextType.PLAIN)]
        delimiter = "*"
        text_type = TextType.BOLD
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertTrue('Closing delimiter not found' in str(context.exception))

    def test_split_nodes_delimiter_invalid_node(self):
        old_nodes = ["This is a *bold* text"]
        delimiter = "*"
        text_type = TextType.BOLD
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertTrue('old_node must be an instance of TextNode' in str(context.exception))

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and another [link](https://another.com)"
        )
        self.assertListEqual([("link", "https://example.com"), ("link", "https://another.com")], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [link](https://another.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "https://another.com"
                ),
            ],
            new_nodes,
    )
    def test_nothing_to_split_image(self):
        node = TextNode("This is text with no images or links", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_nothing_to_split_link(self):
        node = TextNode("This is text with no images or links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_image_start_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an image",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an image", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_link_start_text(self):
        node = TextNode(
            "[link](https://example.com) This is text with a link",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" This is text with a link", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_image_end_text(self):
        node = TextNode(
            "This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_link_end_text(self):
        node = TextNode(
            "This is text with a link [link](https://example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    def test_multiple_nodes_images(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN),
            TextNode(" and some random text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some random text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_multiple_nodes_links(self):
        nodes = [
            TextNode("This is text with a [link](https://example.com)", TextType.PLAIN),
            TextNode(" and some random text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and some random text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_no_collision_images(self):
        node = TextNode("This is a text with a [link](example.com)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a [link](example.com)", TextType.PLAIN)
            ],
            new_nodes,
        )
    
    def test_no_collision_links(self):
        node = TextNode("This is a text with an ![image](example.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ![image](example.com)", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
    
    def test_only_link(self):
        node = TextNode("[link](https://example.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com")
            ],
            new_nodes,
        )

class TestTextToTextNode(unittest.TestCase):
    def test_complete_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,[
        TextNode("This is ", TextType.PLAIN),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.PLAIN),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.PLAIN),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAIN),
        TextNode("link", TextType.LINK, "https://example.com"),
    ])

    def test_plain_sentence(self):
        text = "This is just a sentence"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [TextNode("This is just a sentence", TextType.PLAIN)])

    def test_empty(self):
        text = ''
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [])

    def test_one_markdown_type(self):
        text = "**This is just a bold sentence**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [TextNode("This is just a bold sentence", TextType.BOLD)])

if __name__ == "__main__":
    unittest.main()