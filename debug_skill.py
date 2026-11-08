import re
from pathlib import Path

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text

skill = "c"

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
text = clean_text(extract_text_from_pdf(pdf)).lower()

pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
for m in re.finditer(pattern, text):
    start = max(0, m.start() - 30)
    print("...", text[start:m.end() + 30].replace("\n"," "), "...")