#!/usr/bin/env python3
"""
Book Content Extractor
Extracts and structures content from books for AI processing and analysis.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookMetadata:
    """Represents metadata extracted from a book."""
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    page_count: Optional[int] = None


@dataclass  
class Chapter:
    """Represents a chapter in a book."""
    number: int
    title: str
    content: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None


class BookExtractor:
    """
    Extract content and metadata from various book formats.
    Supports PDF, EPUB, ODT, and plain text files.
    """
    
    SUPPORTED_FORMATS = ['.pdf', '.epub', '.odt', '.txt', '.md']
    
    def __init__(self):
        self.current_file: Optional[Path] = None
        self.metadata: Optional[BookMetadata] = None
        self.chapters: List[Chapter] = []
        
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from a book file.
        
        Args:
            file_path: Path to the book file
            
        Returns:
            Dictionary containing extracted content, metadata, and chapters
        """
        self.current_file = Path(file_path)
        
        if not self.current_file.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        extension = self.current_file.suffix.lower()
        
        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {extension}")
            
        # Extract content based on file type
        if extension == '.pdf':
            content = self._extract_pdf()
        elif extension == '.epub':
            content = self._extract_epub()
        elif extension == '.odt':
            content = self._extract_odt()
        else:  # txt or md
            content = self._extract_text()
            
        # Extract metadata
        self.metadata = self._extract_metadata(content)
        
        # Parse chapters
        self.chapters = self._parse_chapters(content)
        
        return {
            "file": str(self.current_file),
            "format": extension,
            "metadata": self._metadata_to_dict(),
            "content": [{"text": content, "type": "full"}],
            "chapters": self._chapters_to_dict(),
            "stats": self._get_stats(content)
        }
    
    def _extract_pdf(self) -> str:
        """Extract text from PDF file."""
        # Basic PDF text extraction simulation
        # In production, use PyPDF2 or pdfplumber
        return self._simulate_extraction("PDF")
    
    def _extract_epub(self) -> str:
        """Extract text from EPUB file."""
        # Basic EPUB text extraction simulation
        # In production, use ebooklib
        return self._simulate_extraction("EPUB")
    
    def _extract_odt(self) -> str:
        """Extract text from ODT file."""
        # Basic ODT text extraction simulation
        # In production, use odf
        return self._simulate_extraction("ODT")
    
    def _extract_text(self) -> str:
        """Extract text from plain text file."""
        with open(self.current_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _simulate_extraction(self, format_type: str) -> str:
        """Simulate extraction for demonstration."""
        return f"[Extracted {format_type} content from {self.current_file.name}]"
    
    def _extract_metadata(self, content: str) -> BookMetadata:
        """Extract metadata from content."""
        metadata = BookMetadata()
        
        # Try to extract title (first line that's not empty)
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line:
                metadata.title = line[:200]  # Limit title length
                break
                
        # Try to extract author (look for common patterns)
        author_patterns = [
            r'by\s+([^\n]+)',
            r'author:\s*([^\n]+)',
            r'written by\s+([^\n]+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata.author = match.group(1).strip()
                break
                
        # Look for ISBN
        isbn_match = re.search(r'ISBN[:\s-]*([0-9-X]{10,17})', content, re.IGNORECASE)
        if isbn_match:
            metadata.isbn = isbn_match.group(1).strip()
            
        return metadata
    
    def _parse_chapters(self, content: str) -> List[Chapter]:
        """Parse content into chapters."""
        chapters = []
        
        # Split by common chapter patterns
        chapter_patterns = [
            r'^chapter\s+(\d+)',
            r'^chapter\s+([ivxlcdm]+)',
            r'^\d+\.\s+[A-Z]',
            r'^#{1,3}\s+'
        ]
        
        lines = content.split('\n')
        current_chapter = None
        current_content = []
        chapter_num = 1
        
        for line in lines:
            is_chapter_start = False
            
            for pattern in chapter_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    is_chapter_start = True
                    break
                    
            if is_chapter_start and current_chapter:
                # Save previous chapter
                chapters.append(Chapter(
                    number=chapter_num,
                    title=current_chapter,
                    content='\n'.join(current_content)
                ))
                chapter_num += 1
                current_content = []
                
            if is_chapter_start:
                current_chapter = line.strip()
            else:
                current_content.append(line)
                
        # Add last chapter
        if current_chapter or current_content:
            chapters.append(Chapter(
                number=chapter_num,
                title=current_chapter or "Untitled",
                content='\n'.join(current_content)
            ))
            
        # If no chapters found, treat entire content as one chapter
        if not chapters:
            chapters.append(Chapter(
                number=1,
                title="Full Content",
                content=content
            ))
            
        return chapters
    
    def _metadata_to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        if not self.metadata:
            return {}
        return {
            "title": self.metadata.title,
            "author": self.metadata.author,
            "isbn": self.metadata.isbn,
            "publisher": self.metadata.publisher,
            "language": self.metadata.language,
            "page_count": self.metadata.page_count
        }
    
    def _chapters_to_dict(self) -> List[Dict[str, Any]]:
        """Convert chapters to dictionary."""
        return [
            {
                "number": ch.number,
                "title": ch.title,
                "content": ch.content,
                "page_start": ch.page_start,
                "page_end": ch.page_end
            }
            for ch in self.chapters
        ]
    
    def _get_stats(self, content: str) -> Dict[str, Any]:
        """Get content statistics."""
        words = content.split()
        return {
            "characters": len(content),
            "words": len(words),
            "sentences": len(re.split(r'[.!?]+', content)),
            "paragraphs": len([p for p in content.split('\n\n') if p.strip()]),
            "chapters": len(self.chapters)
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract content from books for AI processing"
    )
    parser.add_argument(
        "input",
        help="Path to the book file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file (optional)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "text"],
        default="json",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    extractor = BookExtractor()
    
    try:
        result = extractor.extract(args.input)
        
        if args.format == "json":
            output = json.dumps(result, indent=2)
        else:
            # Text format
            output = f"Title: {result['metadata'].get('title', 'N/A')}\n"
            output += f"Author: {result['metadata'].get('author', 'N/A')}\n"
            output += f"Chapters: {result['stats']['chapters']}\n"
            output += f"Words: {result['stats']['words']}\n\n"
            output += "Content:\n"
            output += result['content'][0]['text'][:5000]
            
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Output written to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {e}", file=__import__('sys').stderr)
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())
