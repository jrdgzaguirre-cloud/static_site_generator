from operator import index
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception('old_node must be an instance of TextNode')
        if isinstance(old_node.text_type, TextType) and old_node.text_type != TextType.PLAIN: 
            new_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text)%2 == 0:
                raise Exception('Closing delimiter not found')
            for i, text in enumerate(split_text):
                if text == '':
                    continue
                if i%2 == 0:
                    new_nodes.append(TextNode(text, TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception('old_node must be an instance of TextNode')
        if isinstance(old_node.text_type, TextType) and old_node.text_type != TextType.PLAIN: 
            new_nodes.append(old_node)
        else:
            extracted_images = extract_markdown_images(old_node.text)
            if not extracted_images:
                new_nodes.append(old_node)
                continue
            remaining_text = old_node.text
            for i in range(len(extracted_images)):
                split_text, remaining_text = remaining_text.split(f"![{extracted_images[i][0]}]({extracted_images[i][1]})", 1)
                if split_text:
                    new_nodes.append(TextNode(split_text, TextType.PLAIN))
                new_nodes.append(TextNode(extracted_images[i][0], TextType.IMAGE, url=extracted_images[i][1]))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes

            
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception('old_node must be an instance of TextNode')
        if isinstance(old_node.text_type, TextType) and old_node.text_type != TextType.PLAIN: 
            new_nodes.append(old_node)
        else:
            extracted_links = extract_markdown_links(old_node.text)
            if not extracted_links:
                new_nodes.append(old_node)
                continue
            remaining_text = old_node.text
            for i in range(len(extracted_links)):
                split_text, remaining_text = remaining_text.split(f"[{extracted_links[i][0]}]({extracted_links[i][1]})", 1)
                if split_text:
                    new_nodes.append(TextNode(split_text, TextType.PLAIN))
                new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, url=extracted_links[i][1]))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    