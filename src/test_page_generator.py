import unittest
import os
import tempfile
from page_generator import *

class TestExtractTitle(unittest.TestCase):
    def test_normal_markdown(self):
        md = """
# This is a header

And a new paragraph
"""

        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a header",
        )

    def test_no_header(self):
        md = """
This is (not) a header

And a new paragraph
"""

        with self.assertRaises(Exception) as context:
            title = extract_title(md)
        self.assertTrue('Markdown requires an h1 header' in str(context.exception))
    
    def test_secondary_header(self):
        md = """
## This is an h2 header

And a new paragraph
"""     
        with self.assertRaises(Exception) as context:
            title = extract_title(md)
        self.assertTrue('Markdown requires an h1 header' in str(context.exception))

    def test_generate_page_uses_normalized_basepath(self):
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = os.path.join(directory, 'index.md')
            template_path = os.path.join(directory, 'template.html')
            output_path = os.path.join(directory, 'docs', 'index.html')
            with open(markdown_path, 'w') as f:
                f.write('# Title\n\n[Contact](/contact)\n\n![Image](/image.png)')
            with open(template_path, 'w') as f:
                f.write('<title>{{ Title }}</title>{{ Content }}')

            generate_page(markdown_path, template_path, output_path, 'project')

            with open(output_path) as f:
                output = f.read()
            self.assertIn('href="/project/contact"', output)
            self.assertIn('src="/project/image.png"', output)

    def test_recursive_generation_ignores_non_markdown_files(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = os.path.join(directory, 'content')
            output_path = os.path.join(directory, 'docs')
            template_path = os.path.join(directory, 'template.html')
            os.mkdir(content_path)
            with open(os.path.join(content_path, 'index.md'), 'w') as f:
                f.write('# Title')
            with open(os.path.join(content_path, '.DS_Store'), 'wb') as f:
                f.write(b'\x80')
            with open(template_path, 'w') as f:
                f.write('<title>{{ Title }}</title>{{ Content }}')

            generate_pages_recursive(content_path, template_path, output_path, '/')

            self.assertTrue(os.path.exists(os.path.join(output_path, 'index.html')))
            self.assertFalse(os.path.exists(os.path.join(output_path, '.DS_Store')))
