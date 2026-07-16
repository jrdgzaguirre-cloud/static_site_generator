from textnode import TextNode, TextType
from copystatic import *
from page_generator import generate_pages_recursive

def main():
    destination_creator('static', 'public')#source_path should be initialized as str: "static" and destination_path to "public"
    generate_pages_recursive('content', 'template.html', 'public')

main()