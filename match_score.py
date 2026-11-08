from pathlib import Path

from sentence_transformers import SentenceTransformer
from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from skill_extractor import extract_skills
from matcher import chunk_text

RELATED = {
    "sql": ["mysql", "postgresql", "sqlite"],
}


def semantic_score(model, resume_text, jd_text):
    """Average best-match similarity between job and resume chunks (0 to 1)."""
    resume_chunks = chunk_text(resume_text)
    jd_chunks = chunk_text(jd_text)

    resume_emb = model.encode(resume_chunks)
    jd_emb = model.encode(jd_chunks)

    scores = model.similarity(jd_emb, resume_emb)
    best = scores.max(dim=1).values
    return max(0.0, float(best.mean()))

def skill_score(resume_text, jd_text):
    """Return skill coverage (0 to 1), matched skills and missing skills."""
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = []
    missing = []
    for skill in sorted(jd_skills):
        options = [skill] + RELATED.get(skill, [])
        if any(option in resume_skills for option in options):
            matched.append(skill)
        else:
            missing.append(skill)


    if not jd_skills:
        return 0.0, matched, missing

    return len(matched) / len(jd_skills), matched, missing


if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")

    pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
    resume_text = clean_text(extract_text_from_pdf(pdf))
    jd_text = clean_text(Path("job_description.txt").read_text(encoding="utf-8"))

    meaning = semantic_score(model, resume_text, jd_text)
    coverage, matched, missing = skill_score(resume_text, jd_text)

    final = 0.7 * coverage + 0.3 * meaning
    total = len(matched) + len(missing)

    print(f"Skill coverage:    {coverage * 100:.0f}%  ({len(matched)} of {total})")
    print(f"Meaning match:     {meaning * 100:.0f}%")
    print(f"FINAL MATCH SCORE: {final * 100:.0f}%")
    print()
    print("Missing skills:", ", ".join(missing))