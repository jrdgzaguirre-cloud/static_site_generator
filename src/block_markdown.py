from enum import Enum
from htmlnode import *
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE ='code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    blocks = []
    for split in splitted:
        stripped = split.strip()
        if stripped != '':
            blocks.append(stripped)    
    return blocks

def block_to_block_type(block) -> BlockType:
    lines = block.split('\n')
    if block.startswith(('# ','## ','### ','#### ','##### ','###### ')):
        return BlockType.HEADING
    
    first_line = lines[0]
    if first_line.startswith('```') and '```' not in first_line[3:] and block.endswith('```'):
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        if not line.startswith('>'):
            is_quote = False
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = True
    for line in lines:
        if not line.startswith('- '):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    count = 1
    for line in lines:    
        if not line.startswith(f'{count}. '):
            is_ordered_list = False
        count += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def block_node_to_html_node(block, block_type: BlockType) -> LeafNode:
    if isinstance(block_type, BlockType):
        if block_type == BlockType.PARAGRAPH:
            children = []
            block = block.replace('\n',' ')
            text_nodes = (text_to_textnodes(block))
            for text_node in text_nodes:
                children.append(text_node_to_html_node(text_node))
            return ParentNode(tag='p', children = children)
        elif block_type == BlockType.HEADING:
            counter = 0           
            for i in range(0,6):
                if block[i] == '#':
                    counter += 1
            block = block[(counter+1):]
            return LeafNode(tag=f'h{counter}', value=block)
        elif block_type == BlockType.QUOTE:
            children = []
            counter = 0
            for line in block.split('\n'):
                child = blocks_children_generator(line, block_type, counter)
                children.extend(child) #iterable, just need one long string
                
                counter += 1
            return ParentNode(tag = 'blockquote', children = children)
        elif block_type == BlockType.CODE:
            _, code = block.split('\n', 1)
            code = code.removesuffix('```')
            return ParentNode(tag = 'pre', children = [text_node_to_html_node(TextNode(code, TextType.CODE))])
        elif block_type == BlockType.UNORDERED_LIST:
            children = []
            counter = 0
            for line in block.split('\n'):
                child = blocks_children_generator(line, block_type, counter)
                children.append(child)
                counter += 1
            return ParentNode(tag = 'ul', children = children)
        elif block_type == BlockType.ORDERED_LIST:
            children = []
            counter = 0
            for line in block.split('\n'):
                child = blocks_children_generator(line, block_type, counter)
                children.append(child)
                counter += 1
            return ParentNode(tag = 'ol', children = children)    
    else:
        raise Exception('block_type must be an instance of BlockType')

def blocks_children_generator(line, block_type, counter):
    html_nodes = []
    if block_type == BlockType.QUOTE:
        if line.startswith('> '):
            line = line.removeprefix('> ')
        if line.startswith('>'):
            line = line.removeprefix('>')
        line_nodes = text_to_textnodes(line)
        for line_node in line_nodes:
            html_nodes.append(text_node_to_html_node(line_node))
        return html_nodes
    if block_type == BlockType.UNORDERED_LIST:
        line = line[2:]
        line_nodes = text_to_textnodes(line)
        for line_node in line_nodes:
            html_nodes.append(text_node_to_html_node(line_node))#appends so can provide tag
        return ParentNode('li', html_nodes)

    if block_type == BlockType.ORDERED_LIST:
        line = line.removeprefix(f'{counter+1}. ')
        line_nodes = text_to_textnodes(line)
        for line_node in line_nodes:
            html_nodes.append(text_node_to_html_node(line_node))
        return ParentNode('li', html_nodes)
    

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child = block_node_to_html_node(block, block_type)
        children.append(child)
    parent = ParentNode('div', children)
    return parent

