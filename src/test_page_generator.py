import unittest
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