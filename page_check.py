from pathlib import Path

import pymupdf

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]

doc_a = pymupdf.open(pdf)
doc_b = pymupdf.open(stream=pdf.read_bytes(), filetype="pdf")


print("Pages:", len(doc_a), len(doc_b))
for i in range(len(doc_a)):
    a = doc_a[i].get_text()
    b = doc_b[i].get_text()
    print(f"Page {i + 1}: path {len(a)} | bytes {len(b)}")