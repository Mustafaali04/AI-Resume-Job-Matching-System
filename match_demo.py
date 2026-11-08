from pathlib import Path

from sentence_transformers import SentenceTransformer
from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from matcher import chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
resume_chunks = chunk_text(clean_text(extract_text_from_pdf(pdf)))

jd_text = Path("job_description.txt").read_text(encoding="utf-8")
jd_chunks = chunk_text(clean_text(jd_text))

resume_emb = model.encode(resume_chunks)
jd_emb = model.encode(jd_chunks)

scores = model.similarity(jd_emb, resume_emb)

best = scores.max(dim=1).values

print("Resume chunks:", len(resume_chunks))
print("Job description chunks:", len(jd_chunks))
for i, s in enumerate(best):
    print(f"JD chunk {i + 1}: best match {float(s):.2f}")
print("Overall similarity:", round(float(best.mean()),2))