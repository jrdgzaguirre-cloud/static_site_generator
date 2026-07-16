from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ''
        props_html = ''
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('LeafNode must have a value')
        if not self.tag:
            return self.value
        if self.props is None or len(self.props) == 0:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError('ParentNode must have a tag')
        if not self.children or len(self.children) == 0:
            raise ValueError('ParentNode must have children')
        html_string = ''
        for child in self.children:
            html_string += child.to_html()
        if self.props is None or len(self.props) == 0:
            return f'<{self.tag}>{html_string}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>'
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if isinstance(text_node.text_type, TextType):
        if text_node.text_type == TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            if not text_node.url:
                raise Exception('TextNode of type LINK must have a url')
            return LeafNode(tag ='a', value = text_node.text, props = {'href': text_node.url})  
        elif text_node.text_type == TextType.IMAGE:
            if not text_node.url:
                raise Exception('TextNode of type IMAGE must have a url')
            return LeafNode(tag = 'img', value = '', props = {'src': text_node.url, 'alt': text_node.text})
    else:
        raise Exception('text_node must be an instance of TextNode')

