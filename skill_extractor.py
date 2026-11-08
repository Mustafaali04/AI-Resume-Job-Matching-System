import re
from pathlib import Path

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from skills_list import SKILLS

def extract_skills(text):
    """Return the skills from SKILLS that appear in the text."""
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.append(skill)

    return found

if __name__ == "__main__":
    pdf_files = list(Path("sample_resumes").glob("*.pdf"))

    if not pdf_files:
        print("N PDF found in the sampe_resumes folder.")
        raise SystemExit

    raw_text = extract_text_from_pdf(pdf_files[0])
    cleaned = clean_text(raw_text)
    found = extract_skills(cleaned)

    print("Skills found:", len(found), "out of", len(SKILLS))
    for skill in found:
        print("-", skill)