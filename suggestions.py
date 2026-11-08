from pathlib import Path

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from match_score import skill_score

TIPS = {
    "pandas": "Build a small project that cleans and analyses a CSV file with pandas.",
    "numpy": "Practise array operations with NumPy and use it inside an ML project.",
    "scikit-learn": "Train a regression or classification model on a public dataset with scikit-learn.",
    "deep learning": "Build a small neural network, such as an image classifier.",
    "tensorflow": "Follow a beginner TensorFlow/Keras tutorial and keep the notebook on GitHub.",
    "pytorch": "Implement a simple model in PyTorch. Learning one of TensorFlow or PyTorch is a good start.",
}


def make_suggestions(missing):
    """Return one tip for each missing skill."""
    suggestions = []
    for skill in missing:
        default = f"Learn the basics of {skill} and build a small project that uses it."
        tip = TIPS.get(skill, default)
        suggestions.append(f"{skill}: {tip}")
    return suggestions


if __name__ == "__main__":
    pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
    resume_text = clean_text(extract_text_from_pdf(pdf))
    jd_text = clean_text(Path("job_description.txt").read_text(encoding="utf-8"))


    coverage, matched, missing, = skill_score(resume_text, jd_text)


    print("Improvement suggestions:")
    for number, line in enumerate(make_suggestions(missing), start=1):
        print(f"{number}. {line}")