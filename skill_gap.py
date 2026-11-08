from pathlib import Path

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from skill_extractor import extract_skills

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
resume_text = clean_text(extract_text_from_pdf(pdf))

jd_text = clean_text(Path("job_description.txt").read_text(encoding="utf-8"))

resume_skills = set(extract_skills(resume_text))
jd_skills = set(extract_skills(jd_text))

matched = sorted(jd_skills & resume_skills)
missing = sorted(jd_skills - resume_skills)

print("Skills the job asks for:", len(jd_skills))
print()
print("YOU HAVE (", len(matched), "):")
for skill in matched:
    print("  +", skill)
print()
print("MISSING (", len(missing), "):")
for skill in missing:
    print("  -", skill)