"""Safe extraction helpers for user-uploaded healthcare documents."""

from io import BytesIO
from pathlib import Path


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF, DOCX, or plain-text files.

    Scanned/image-only PDFs may return little or no text; this function does not
    attempt to invent OCR content.
    """
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF support requires the pypdf package.") from exc

        reader = PdfReader(BytesIO(file_bytes))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append(f"[Page {index}]\n{text}")
        return "\n\n".join(pages).strip()

    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("DOCX support requires the python-docx package.") from exc

        document = Document(BytesIO(file_bytes))
        parts = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        return "\n".join(parts).strip()

    if suffix in {".txt", ".md", ".csv"}:
        return file_bytes.decode("utf-8", errors="replace").strip()

    raise ValueError("Unsupported document type. Upload PDF, DOCX, TXT, MD, or CSV.")


def extract_text(file_path: str) -> str:
    """Backward-compatible path-based extraction helper."""
    path = Path(file_path)
    return extract_text_from_bytes(path.read_bytes(), path.name)
