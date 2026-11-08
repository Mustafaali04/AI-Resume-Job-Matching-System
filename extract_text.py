from pathlib import Path
import pymupdf

pdf_files = list(Path("sample_resumes").glob("*.pdf"))

if not pdf_files:
    print("No PDF found in the sample_resumes folder.")
    raise SystemExit

pdf_path = pdf_files[0]
print("Reading:", pdf_path.name)

doc = pymupdf.open(pdf_path)
print("Number of pages:", len(doc))

text = ""
for page in doc:
    text += page.get_text()

doc.close()

print("Characters extracted:", len(text))
print("---- First 500 characters ----")
print(text[:500])