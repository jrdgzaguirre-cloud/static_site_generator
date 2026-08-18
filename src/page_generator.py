import os
from block_markdown import *


def normalize_basepath(basepath):
    return f"/{basepath.strip('/')}" + ("/" if basepath.strip('/') else "")

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith('# '):
        blocks[0] = blocks[0].removeprefix('# ')
        return blocks[0]
    else:
        raise Exception('Markdown requires an h1 header')       

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}') 
    with open(from_path) as f:
        text = f.read()
    with open(template_path) as t:
        template = t.read()
    html_node = markdown_to_html_node(text)
    content = html_node.to_html()
    title = extract_title(text)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', content)
    basepath = normalize_basepath(basepath)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(from_path, template_path, dest_path, basepath):
    if os.path.isfile(from_path):
        if from_path.endswith('.md'):
            html_dest_path = os.path.splitext(dest_path)[0] + '.html'
            generate_page(from_path, template_path, html_dest_path, basepath)
        return

    for item in os.listdir(from_path):
        if item.startswith('.'):
            continue
        new_path = os.path.join(from_path, item)
        new_dest_path = os.path.join(dest_path, item)
        generate_pages_recursive(new_path, template_path, new_dest_path, basepath)
