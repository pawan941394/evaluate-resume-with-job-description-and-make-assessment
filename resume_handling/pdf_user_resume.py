import os
import sys
from typing import Optional
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text

def _get_pdfminer_extractor():
    """
    Returns pdfminer.high_level.extract_text or raises informative ImportError.
    """
    try:

        return extract_text
    except ImportError:
        raise ImportError(
            "pdfminer.six not installed. Install with: pip install pdfminer.six\n"
            "Current import failed for module 'pdfminer.high_level'."
        )


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract full text from a PDF file.
    Returns cleaned text; raises FileNotFoundError or ValueError on issues.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Input file must be a .pdf")

    try:
        extract_text_func = _get_pdfminer_extractor()
        text = extract_text_func(pdf_path) or ""
    except Exception as e:
        raise RuntimeError(f"Primary extraction failed: {e}")

    text = text

    if not text.strip():
        # Optional secondary attempt (PyPDF2)
        try:

            reader = PdfReader(pdf_path)
            pages = []
            for p in reader.pages:
                try:
                    pages.append(p.extract_text() or "")
                except Exception:
                    pages.append("")
            fallback_text = "\n".join(pages)
            fallback_text = fallback_text
            if fallback_text.strip():
                text = fallback_text
        except Exception:
            pass  # Keep original (empty) if fallback also fails

    return text


def flatten_text(text: str) -> str:
    """
    Replace newlines with spaces and collapse repeated whitespace.
    """
    # Replace newlines with space
    flat = text.replace("\r", "\n").replace("\n", " ")
    # Collapse multiple spaces
    return " ".join(flat.split())


def preserve_line_structure(text: str) -> str:
    """
    Keep original line breaks; trim and collapse spaces within each line only.
    """
    lines = text.replace("\r", "\n").split("\n")
    cleaned = [(" ".join(l.split())) for l in lines]
    return "\n".join(cleaned)


def get_pdf_details(pdf_path: str) -> dict:
    """
    Return dict with raw text, flattened text, page_count, file_size_bytes.
    """
    raw = extract_pdf_text(pdf_path)
    # Page count
    try:
        

        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
    except Exception:
        page_count = None
    size_bytes = os.path.getsize(pdf_path)
    return {
        "raw_text": raw,
        "text_preserved": preserve_line_structure(raw),
        "text_flat": flatten_text(raw),
        "page_count": page_count,
        "file_size_bytes": size_bytes,
    }


def main(provide_rsume_path: Optional[str] = None):
    # Allow path override via CLI argument
    default_path = provide_rsume_path
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else default_path
    try:
        details = get_pdf_details(pdf_path)
        return details["text_flat"]
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


