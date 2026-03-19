# Book Content Extractor

## Description

This tool extracts and structures content from books for AI processing and analysis. It supports multiple format, including PDF, EPUB, and text formats.

## Features

- Extract text from PDF, EPUB, ODT and text files
- Parse and segment content by chapter/page
- Extract metadata (author, title, ISBN, publisher)
- Detect and extract chapters
- Give text representation - Optimized text for AI-use
- Text post-extraction and summarization

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from book_content_extractor import BookExtractor


# Initialize the extractor
extractor = BookExtractor()

# Extract from a PDF
data = extractor.extract("path/to/book.pdf")
print(data["content"][0]["text"])

# Extract from an EPUB
data = extractor.extract("path/to/book.epub")
print(data["content"][0]["text"])

# Extract metadata
details = extractor.get_metadata("path/to/book.pdf")
print(details["title"])
print(details["author"])
```

## API Example

```python
# Create API application from book_content_extractor
from book_content_extractor import BookExtractor, App
from hello import HonoApp
import json

app = HonoApp("Book Content Extractor")

extractor = BookExtractor()

@app.route("/extract", methods=["POST"])
def extract_book():
    request = app.request()
    book_path = request.form.get("book_path")
    if not book_path:
        return json({"error": "Book path required"}, 400)

    result = extractor.extract(book_path)
    return json(result)

if __name__ == "__main__":
    app.run()
```

## License

MIT License - see LICENSE.md
