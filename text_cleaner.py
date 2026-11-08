import re
from pathlib import Path

from resume_parser import extract_text_from_pdf


def clean_text(text):
    """Tidy extracted text: fix spacing and remove blank lines."""
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+"," ",text)
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    text = "\n".join(lines)
    text = re.sub(r"([A-Za-z])-\n([a-z])", r"\1\2", text)
    return text

if __name__ == "__main__":
    pdf_files = list(Path("sample_resumes").glob("*.pdf"))

    if not pdf_files:
        print("No PDF found in the sample_resumes folder.")
        raise SystemExit

    raw_text = extract_text_from_pdf(pdf_files[0])
    cleaned = clean_text(raw_text)

    print("Characters before cleaning:", len(raw_text))
    print("Characters after cleaning:", len(cleaned))
    print("---- First 300 characters (cleaned) ----")
    print(cleaned[:300])