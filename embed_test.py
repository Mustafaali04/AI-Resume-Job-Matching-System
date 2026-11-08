from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I build machine learning models using Python.",
    "Looking for a Python developer with ML experience.",
    "I enjoy cooking pasta on weekends.",
]

embeddings = model.encode(sentences)
print("Embeddings shape:", embeddings.shape)

scores = model.similarity(embeddings, embeddings)
print("Sentence 1 vs 2:", round(float(scores[0][1]), 2))
print("Sentence 1 vs 3:", round(float(scores[0][2]), 2))