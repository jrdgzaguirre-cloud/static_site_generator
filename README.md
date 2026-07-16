# Static Site Generator

A simple static site generator built in Python that converts Markdown files into a static HTML website.

## Features

- Converts Markdown to HTML
- Supports headings, paragraphs, lists, code blocks, blockquotes, bold/italic text, links, and images
- Recursively copies static assets (CSS, images) to the output directory
- Generates a full site from a content directory of Markdown files

## Usage

1. Clone the repository
2. Add your Markdown content to the `content` directory
3. Run the build/dev script:

​```bash
./main.sh
​```

4. Open the generated site in your browser

## Testing

Run the test suite with:

​```bash
./test.sh
​```

## Project Structure

- `content/` - Markdown source files
- `static/` - CSS, images, and other assets
- `src/` - Python source code
- `docs/` (or `public/`) - generated output

## Known Limitations

- Nested/combined inline markdown (e.g. `**_bold and italic_**`) is not supported. Only single-style inline formatting works correctly (bold, italic, code, links, images).

