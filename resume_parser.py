from pathlib import Path
import pymupdf


def _doc_to_text(doc):
    """Read every page of an open PDF and return the text as one string."""
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text


def extract_text_from_pdf(pdf_path):
    """Return all the text of a PDF file as one string."""
    return _doc_to_text(pymupdf.open(pdf_path))


def extract_text_from_bytes(pdf_bytes):
    """Return all the text of a PDF given as bytes (used for uploaded files)."""
    return _doc_to_text(pymupdf.open(stream=pdf_bytes, filetype="pdf"))

    

if __name__ == "__main__":
    pdf_files = list(Path("sample_resumes").glob("*.pdf"))

    if not pdf_files:
        print("No PDF found in the sample_resumes folder.")
        raise SystemExit

    pdf_path = pdf_files[0]
    text = extract_text_from_pdf(pdf_path)

    print("Reading:", pdf_path.name)
    print("Characters extracted:", len(text))
    print("---- First 300 characters ----")
    print(text[:300])