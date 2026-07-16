from textnode import TextNode, TextType
from copystatic import *
from page_generator import generate_pages_recursive
import sys

def main():
    if sys.argv[0]:
        basepath = sys.argv[0]
    else: 
        basepath = '/'
    destination_creator('static', 'docs')#source_path should be initialized as str: "static" and destination_path to "docs"
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

main()