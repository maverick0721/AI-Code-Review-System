from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "Avoid SQL injection by using parameterized queries.",
    "Never store passwords in plain text.",
    "Validate all user inputs.",
    "Avoid hardcoded credentials."
]

embeddings = model.encode(docs)

index = faiss.IndexFlatL2(embeddings.shape[1])

index.add(np.array(embeddings))


def retrieve_context(query, k=2):

    q_emb = model.encode([query])

    D, I = index.search(np.array(q_emb), k)

    return "\n".join([docs[i] for i in I[0]])