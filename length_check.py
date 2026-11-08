from pathlib import Path

from sentence_transformers import SentenceTransformer
from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model max length (tokens):", model.max_seq_length)

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
text = clean_text(extract_text_from_pdf(pdf))

tokens = model.tokenizer(text)["input_ids"]
print("Resume length (tokens):", len(tokens))