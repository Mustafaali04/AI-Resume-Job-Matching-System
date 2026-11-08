import streamlit as st
from html import escape
from sentence_transformers import SentenceTransformer

from resume_parser import extract_text_from_bytes
from text_cleaner import clean_text
from match_score import semantic_score, skill_score
from suggestions import make_suggestions
from ai_helper import make_ai_suggestions
from resume_check import looks_like_resume

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

@property --p { syntax: '<number>'; inherits: false; initial-value: 0; }
@keyframes fillRing { from { --p: 0; } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

html, body, .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
.stApp button, .stApp textarea, .stApp input {
  font-family: 'Inter', 'Segoe UI', sans-serif;
}
.block-container { padding-top: 2rem; max-width: 900px; }
.stApp {
  background:
    radial-gradient(rgba(148,163,184,0.10) 1px, transparent 1px) 0 0 / 24px 24px,
    radial-gradient(circle at 15% 0%, #1E1B4B 0%, #0F172A 45%, #020617 100%);
}
[data-testid="stHeader"] { background: transparent; }

.banner { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
          gap: 1.5rem; padding: 2rem 2.25rem; border-radius: 20px; margin-bottom: 1.5rem;
          background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
          box-shadow: 0 10px 30px rgba(79,70,229,0.35); color: white; }
.banner-text { flex: 1 1 320px; }
.banner-tag { font-size: 0.75rem; letter-spacing: 0.18em; font-weight: 600;
              opacity: 0.85; margin-bottom: 0.5rem; }
.banner h1 { margin: 0; padding: 0; font-size: 2.4rem; line-height: 1.15; color: white; }
.banner p { margin: 0.7rem 0 0 0; opacity: 0.92; max-width: 30rem; }
.badge { text-align: center; }
.badge-ring { width: 128px; height: 128px; border-radius: 50%; margin: 0 auto;
              display: flex; align-items: center; justify-content: center;
              background: conic-gradient(#FFFFFF 0 67%, rgba(255,255,255,0.25) 0); }
.badge-inner { width: 98px; height: 98px; border-radius: 50%; background: rgba(15,23,42,0.88);
               display: flex; align-items: center; justify-content: center;
               font-size: 2rem; font-weight: 700; color: white; }
.badge-note { margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.85; letter-spacing: 0.08em; }

.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
         gap: 1rem; margin-bottom: 1.5rem; }
.step { padding: 1.1rem 1.25rem; border-radius: 16px; background: rgba(30,41,59,0.85);
        border: 1px solid #334155; }
.step-num { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center;
            justify-content: center; font-weight: 700; color: white; margin-bottom: 0.6rem;
            background: linear-gradient(135deg, #4F46E5, #06B6D4); }
.step-title { font-weight: 600; color: #F8FAFC; }
.step-text { color: #94A3B8; font-size: 0.9rem; margin-top: 0.2rem; }

[data-testid="stFileUploaderDropzone"] {
  border: 2px dashed #6366F1; border-radius: 16px; padding: 1.6rem;
  background: rgba(30,41,59,0.6); transition: all 0.2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #06B6D4; box-shadow: 0 0 0 4px rgba(6,182,212,0.18);
}

.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg, #4F46E5, #06B6D4); border: none; color: white;
  font-weight: 600; padding: 0.6rem 1.8rem; border-radius: 12px;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
  transform: translateY(-2px); box-shadow: 0 8px 20px rgba(79,70,229,0.45); color: white;
}

[data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; }
button[data-baseweb="tab"] { border-radius: 999px; padding: 0.4rem 1.1rem; height: auto;
                             background: rgba(30,41,59,0.7); border: 1px solid #334155; }
button[data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, #4F46E5, #06B6D4); border-color: transparent;
}
button[data-baseweb="tab"][aria-selected="true"] p { color: white; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

.fade-in { animation: fadeIn 0.6s ease both; }
.card { padding: 1.25rem 1.5rem; border-radius: 16px; margin-bottom: 1rem;
        background: rgba(30,41,59,0.85); border: 1px solid #334155; }
.ring-card { display: flex; align-items: center; gap: 1.5rem; }
.ring { width: 120px; height: 120px; border-radius: 50%; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        background: conic-gradient(var(--c) calc(var(--p) * 1%), #334155 0);
        animation: fillRing 1.2s ease-out; }
.ring-inner { width: 92px; height: 92px; border-radius: 50%; background: #0F172A;
              display: flex; align-items: center; justify-content: center;
              font-size: 1.9rem; font-weight: 700; color: white; }
.verdict { font-size: 1.7rem; font-weight: 700; line-height: 1.2; }
.verdict-note { opacity: 0.7; font-size: 0.85rem; margin-top: 0.3rem; }
.score-label { opacity: 0.7; font-size: 0.9rem; margin-bottom: 0.4rem; }
.score-number { font-weight: 700; line-height: 1; }
.bar { height: 10px; border-radius: 999px; background: #334155;
       margin-top: 0.8rem; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; }

.stats { margin: 0.5rem 0 1rem 0; }
.stat { display: inline-block; padding: 0.3rem 0.9rem; margin: 0.2rem 0.4rem 0.2rem 0;
        border-radius: 999px; font-size: 0.85rem; font-weight: 600; color: #E2E8F0;
        background: rgba(148,163,184,0.15); border: 1px solid #475569; }
.stat-have { color: #34D399; background: rgba(16,185,129,0.15); border-color: #10B981; }
.stat-miss { color: #F87171; background: rgba(239,68,68,0.15); border-color: #EF4444; }

.chip { display: inline-block; padding: 0.25rem 0.75rem; margin: 0.2rem 0.3rem 0.2rem 0;
        border-radius: 999px; font-size: 0.85rem; font-weight: 500; }
.chip-have { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid #10B981; }
.chip-miss { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid #EF4444; }

.tip-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.9rem; }
.tip-card { padding: 1rem 1.2rem; border-radius: 14px; background: rgba(30,41,59,0.85);
            border: 1px solid #334155; border-left: 4px solid #06B6D4; }
.tip-skill { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em;
             text-transform: uppercase; color: #67E8F9; margin-bottom: 0.4rem; }
.tip-text { color: #E2E8F0; font-size: 0.92rem; line-height: 1.45; }

.footer { text-align: center; margin-top: 3rem; padding-top: 1rem;
          border-top: 1px solid #334155; color: #94A3B8; font-size: 0.85rem; }
.footer a { color: #A5B4FC; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def score_color(value):
    if value >= 0.7:
        return "#10B981"
    if value >= 0.4:
        return "#F59E0B"
    return "#EF4444"


def verdict_text(value):
    if value >= 0.7:
        return "Strong match"
    if value >= 0.4:
        return "Partial match"
    return "Weak match"


def score_card(label, value):
    if value is None:
        text, percent, color = "N/A", 0, "#94A3B8"
    else:
        percent = min(100, max(0, round(value * 100)))
        text, color = f"{percent}%", score_color(value)
    return (
        f'<div class="card fade-in"><div class="score-label">{label}</div>'
        f'<div class="score-number" style="font-size:2rem; color:{color}">{text}</div>'
        f'<div class="bar"><div class="bar-fill" '
        f'style="width:{percent}%; background:{color}"></div></div></div>'
    )


def ring_card(value, verdict):
    percent = min(100, max(0, round(value * 100)))
    color = score_color(value)
    return (
        '<div class="card ring-card fade-in">'
        f'<div class="ring" style="--p:{percent}; --c:{color};">'
        f'<div class="ring-inner">{percent}%</div></div>'
        "<div>"
        '<div class="score-label">Final match score</div>'
        f'<div class="verdict" style="color:{color}">{escape(verdict)}</div>'
        '<div class="verdict-note">70% skills + 30% meaning</div>'
        "</div></div>"
    )


def chips(skills, css_class):
    return "".join(f'<span class="chip {css_class}">{escape(s)}</span>' for s in skills)


def stat_pills(matched, missing, total):
    if total == 0:
        return '<div class="stats"><span class="stat">0 known skills found in the job</span></div>'
    return (
        '<div class="stats">'
        f'<span class="stat stat-have">{len(matched)} matched</span>'
        f'<span class="stat stat-miss">{len(missing)} missing</span>'
        f'<span class="stat">{total} skills in the job</span>'
        "</div>"
    )


def tip_cards(tips):
    cards = []
    for tip in tips:
        skill, sep, text = tip.partition(":")
        if not sep:
            skill, text = "Tip", tip
        safe_skill = escape(skill.strip())
        safe_text = escape(text.strip()).replace("$", "&#36;")
        cards.append(
            '<div class="tip-card">'
            f'<div class="tip-skill">{safe_skill}</div>'
            f'<div class="tip-text">{safe_text}</div>'
            "</div>"
        )
    return '<div class="tip-grid">' + "".join(cards) + "</div>"


def step_cards():
    return (
        '<div class="steps">'
        '<div class="step"><div class="step-num">1</div>'
        '<div class="step-title">Upload</div>'
        '<div class="step-text">Add your resume as a PDF.</div></div>'
        '<div class="step"><div class="step-num">2</div>'
        '<div class="step-title">Paste</div>'
        '<div class="step-text">Paste the job description you want to match.</div></div>'
        '<div class="step"><div class="step-num">3</div>'
        '<div class="step-title">Analyze</div>'
        '<div class="step-text">Get a score, your skill gaps and tips.</div></div>'
        "</div>"
    )


def build_report(r):
    no_skills = r["total_skills"] == 0
    coverage = "N/A" if no_skills else f"{r['coverage'] * 100:.0f}%"
    lines = [
        "AI Resume & Job Matcher - match report",
        "",
        f"Job: {r['job_title']}",
        f"Final match score: {r['final'] * 100:.0f}% ({r['verdict']})",
        f"Skill coverage: {coverage}",
        f"Meaning match: {r['meaning'] * 100:.0f}%",
        "",
        "Skills you have: " + (", ".join(r["matched"]) or "none"),
        "Missing skills: " + (", ".join(r["missing"]) or "none"),
    ]
    if r["tips"]:
        lines.append("")
        lines.append(f"Improvement tips ({r['source']}):")
        lines.extend("- " + tip for tip in r["tips"])
    return "\n".join(lines)


def analyze(resume_file, job_text, use_ai):
    """Run the whole analysis. Return a result dict, or None if it failed."""
    error = None
    result = None

    with st.status("Analyzing your resume...", expanded=True) as status:
        st.write("Reading the PDF...")
        resume_text = clean_text(extract_text_from_bytes(resume_file.getvalue()))

        if not resume_text.strip():
            error = "No text found in this PDF. It may be a scanned image."
            status.update(label="Could not read the PDF", state="error")
        else:
            st.write("Finding skills...")
            jd_text = clean_text(job_text)
            coverage, matched, missing = skill_score(resume_text, jd_text)

            st.write("Comparing meaning (the first run loads the model, so it takes longer)...")
            meaning = semantic_score(load_model(), resume_text, jd_text)

            job_title = job_text.strip().splitlines()[0][:80]
            tips, source = [], ""
            if missing:
                st.write("Writing improvement tips...")
                if use_ai:
                    tips, source = make_ai_suggestions(missing, job_title)
                else:
                    tips, source = make_suggestions(missing), "built-in tips"

            total_skills = len(matched) + len(missing)
            final = 0.7 * coverage + 0.3 * meaning
            verdict = verdict_text(final)
            if total_skills < 3:
                verdict += " (low confidence)"

            status.update(label="Analysis complete", state="complete", expanded=False)
            result = {
                "final": final,
                "coverage": coverage,
                "meaning": meaning,
                "matched": matched,
                "missing": missing,
                "total_skills": total_skills,
                "verdict": verdict,
                "looks_like_resume": looks_like_resume(resume_text),
                "job_title": job_title,
                "tips": tips,
                "source": source,
            }

    if error:
        st.error(error)
    return result


def show_results(r):
    total = r["total_skills"]
    no_skills = total == 0

    st.caption(
        "Showing the result of your last analysis. "
        "Click Analyze again after changing the resume or the job description."
    )

    if not r["looks_like_resume"]:
        st.warning(
            "This PDF does not look like a resume (few sections such as Education, "
            "Skills or Projects were found). The score may not be meaningful."
        )

    if 0 < total < 3:
        st.warning(
            f"Only {total} known skill(s) were found in the job description, "
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
    st.markdown(ring_card(r["final"], r["verdict"]), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(
        score_card("Skill coverage", None if no_skills else r["coverage"]),
        unsafe_allow_html=True,
    )
    col2.markdown(score_card("Meaning match", r["meaning"]), unsafe_allow_html=True)

    st.markdown(stat_pills(r["matched"], r["missing"], total), unsafe_allow_html=True)

    tab_skills, tab_tips = st.tabs(["Skills", "How to improve"])

    with tab_skills:
        st.markdown("**Skills you have**")
        if no_skills:
            st.write("No known skills were detected in the job description.")
        elif r["matched"]:
            st.markdown(chips(r["matched"], "chip-have"), unsafe_allow_html=True)
        else:
            st.write("None found")

        st.markdown("**Missing skills**")
        if no_skills:
            st.write("Cannot be checked, because no known skills were detected in the job description.")
        elif r["missing"]:
            st.markdown(chips(r["missing"], "chip-miss"), unsafe_allow_html=True)
        else:
            st.write("None. You cover every skill the job asks for.")

    with tab_tips:
        if not r["missing"]:
            st.write("Nothing to improve for the skills listed in this job description.")
        else:
            st.caption(f"Tips source: {r['source']}")
            st.markdown(tip_cards(r["tips"]), unsafe_allow_html=True)

    st.download_button(
        "Download report",
        data=build_report(r),
        file_name="match_report.txt",
        mime="text/plain",
    )


st.markdown(
    '<div class="banner">'
    '<div class="banner-text">'
    '<div class="banner-tag">AI RESUME MATCHER</div>'
    "<h1>Does your resume fit the job?</h1>"
    "<p>Upload your resume, paste a job description, and get a match score, "
    "your missing skills, and tips to close the gaps.</p>"
    "</div>"
    '<div class="badge">'
    '<div class="badge-ring"><div class="badge-inner">67%</div></div>'
    '<div class="badge-note">SAMPLE RESULT</div>'
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

if st.session_state.get("result") is None:
    st.markdown(step_cards(), unsafe_allow_html=True)

resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_text = st.text_area("Paste the job description here", height=200)
use_ai = st.checkbox("Use AI for improvement tips (optional, tick before clicking Analyze)")

if st.button("Analyze", type="primary"):
    if resume_file is None:
        st.warning("Please upload a resume.")
    elif not job_text.strip():
        st.warning("Please paste a job description.")
    else:
        st.session_state.pop("result", None)
        new_result = analyze(resume_file, job_text, use_ai)
        if new_result is not None:
            st.session_state["result"] = new_result

saved = st.session_state.get("result")
if saved is not None:
    show_results(saved)

st.markdown(
    '<div class="footer">Built by Mohammed Mustafa Ali · '
    '<a href="https://github.com/Mustafaali04/AI-Resume-Job-Matching-System" target="_blank">GitHub</a><br>'
    "This app does not save uploaded resumes. "
    "Please avoid uploading sensitive documents to a public demo."
    "</div>",
    unsafe_allow_html=True,
)