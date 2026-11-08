import streamlit as st
from sentence_transformers import SentenceTransformer

from resume_parser import extract_text_from_bytes
from text_cleaner import clean_text
from match_score import semantic_score, skill_score
from suggestions import make_suggestions
from ai_helper import make_ai_suggestions
from resume_check import looks_like_resume

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


st.title("AI Resume & Job Matching System")
st.write("Upload your resume and paste a job description to see how well they match.")

resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_text = st.text_area("Paste the job description here", height=200)
use_ai = st.checkbox("Use AI for improvement tips (optional)")


if not st.button("Analyze"):
    st.stop()

if resume_file is None:
    st.warning("Please upload a resume.")
    st.stop()

if not job_text.strip():
    st.warning("Please paste a job description.")
    st.stop()

with st.spinner("Analyzing... the first run takes longer while the model loads."):
    resume_text = clean_text(extract_text_from_bytes(resume_file.getvalue()))
    jd_text = clean_text(job_text)


    if not resume_text.strip():
        st.error("No text found in this PDF. It may be a scanned image.")
        st.stop()


    model = load_model()
    meaning = semantic_score(model, resume_text, jd_text)
    coverage, matched, missing = skill_score(resume_text, jd_text)


if not looks_like_resume(resume_text):
    st.warning(
        "This PDF does not look like a resume (few sections such as Education, "
        "Skills or Projects were found). The score may not be meaningful."
    )


final = 0.7 * coverage + 0.3 * meaning
no_skills = not matched and not missing
total_skills = len(matched) + len(missing)

if 0 < total_skills < 3:
    st.warning(
        f"Only {total_skills} known skill(s) were found in the job description, "
        "so the skill coverage is based on very little information and the "
        "score may look higher than it should."
    )

if no_skills:
    st.warning(
        "No known skills were found in the job description, so skill coverage "
        "cannot be measured. The score below counts only the meaning match, "
        "at 30% weight, so it will be low."
    )

st.subheader("Results")
st.metric("Final match score", f"{final * 100:.0f}%")


col1, col2 = st.columns(2)
col1.metric("Skill coverage", "N/A" if no_skills else f"{coverage * 100:.0f}%")
col2.metric("Meaning match", f"{meaning * 100:.0f}%")


st.subheader("Skills you have")
if no_skills:
    st.write("No known skills were detected in the job description.")
else:
    st.write(", ".join(matched) if matched else "None found")

st.subheader("Missing skills")
if no_skills:
    st.write("Cannot be checked, because no known skills were detected in the job description.")
else:
    st.write(", ".join(missing) if missing else "None. You cover every skill the job asks for.")

if missing:
    st.subheader("How to improve")
    job_title = job_text.strip().splitlines()[0]
    if use_ai:
        tips, source = make_ai_suggestions(missing, job_title)
    else:
        tips, source = make_suggestions(missing), "built-in tips"
    st.caption(f"Tips source: {source}")
    for tip in tips:
        st.write("- " + tip)