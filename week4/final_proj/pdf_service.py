from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {file_path}")

    reader = PdfReader(path)

    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages_text.append(page_text)

    text = "\n".join(pages_text).strip()

    if not text:
        raise RuntimeError("No text extracted from PDF.")

    return text