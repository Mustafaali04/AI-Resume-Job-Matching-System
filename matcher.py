from pathlib import Path

from sentence_transformers import SentenceTransformer
from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text


def chunk_text(text, max_words=120):
    """Split text into chunks of about max_words words, keeping lines together."""
    chunks = []
    current = []
    count = 0

    for line in text.split("\n"):
        words = len(line.split())
        if current and count + words > max_words:
            chunks.append("\n".join(current))
            current = []
            count = 0
        current.append(line)
        count += words

    if current:
        chunks.append("\n".join(current))

    return chunks


if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")

    pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
    text = clean_text(extract_text_from_pdf(pdf))
    chunks = chunk_text(text)

    print("Text length (characters):", len(text))
    print("Number of chunks:", len(chunks))

    if not chunks:
        print("No chunks were created. Check the text above.")
        raise SystemExit

    lengths = [len(model.tokenizer(c)["input_ids"]) for c in chunks]
    print("Tokens per chunk:", lengths)
    print("Longest chunk:", max(lengths), "tokens (limit is 256)")
