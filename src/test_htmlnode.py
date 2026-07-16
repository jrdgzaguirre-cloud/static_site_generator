import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag = 'div', value = 'Hello', props = {})
        self.assertEqual(node.props_to_html(), '')
    def test_props_to_html_none(self):
        node = HTMLNode(tag = 'div', value = 'Hello', props = None)
        self.assertEqual(node.props_to_html(), '')
    def test_props_to_html_single(self):
        node = HTMLNode(tag = 'div', value = 'Hello', props = {'class': 'my-class'})
        self.assertEqual(node.props_to_html(), ' class="my-class"')
    def test_props_to_html_multiple(self):
        node = HTMLNode(tag = 'div', value = 'Hello', props = {'class': 'my-class', 'id': 'my-id'})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here!", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_props(self):
        child_node = LeafNode("span", "child", props={"class": "child-class"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span class="child-class">child</span></div>')

    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("b", "grandchild", props={"class": "grandchild-class"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b class="grandchild-class">grandchild</b></span></div>',
        )
    
    def test_to_html_with_grandchildren_props_child(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], props={"class": "grandchild-class"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span class="grandchild-class"><b>grandchild</b></span></div>',
        )

class TestTextNodeToHTMLNode(unittest.TestCase):    
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK , url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "This is an image"})

if __name__ == "__main__":
    unittest.main()