import re
from pathlib import Path

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text

HEADINGS = [
    "education", "skill", "experience", "project", "internship",
    "certification", "achievement", "summary", "objective", "about me",
    "profile",
]


def find_headings(text):
    """Return the resume headings found on short lines of the text."""
    found = set()
    for line in text.lower().split("\n"):
        words = re.findall(r"[a-z]+", line)
        if 0 < len(words) <= 4:
            for heading in HEADINGS:
                if heading in line:
                    found.add(heading)
    return found


def looks_like_resume(text, minimum=3):
    """True if the text has at least 'minimun' resume headings."""
    return len(find_headings(text)) >=minimum


if __name__ == "__main__":
    for pdf in Path("sample_resumes").rglob("*.pdf"):
        text = clean_text(extract_text_from_pdf(pdf))
        found = sorted(find_headings(text))
        print(pdf.name, "->", len(found), "headings:", found)