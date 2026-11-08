from pathlib import Path

from resume_parser import extract_text_from_pdf, extract_text_from_bytes

for pdf in Path("sample_resumes").glob("*.pdf"):
    from_path = len(extract_text_from_pdf(pdf))
    from_bytes = len(extract_text_from_bytes(pdf.read_bytes()))
    print(pdf.name, "| path:", from_path, "| bytes:", from_bytes)