from pathlib import Path
import re

from sentence_transformers import SentenceTransformer, util

KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "devops_troubleshooting.md"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None
_documents = None
_embeddings = None


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return []

    content = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", content)[1:]

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def _get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME, device="cpu")

    return _model


def retrieve_knowledge(query: str, top_k: int = 2):
    global _documents, _embeddings

    if not query or not query.strip():
        return []

    if _documents is None:
        _documents = load_knowledge()

        if not _documents:
            return []

        _embeddings = _get_model().encode(
            _documents,
            convert_to_tensor=True
        )

    query_embedding = _get_model().encode(
        query,
        convert_to_tensor=True
    )

    scores = util.cos_sim(query_embedding, _embeddings)[0]
    ranked_indices = scores.argsort(descending=True).tolist()

    ranked_scores = [
        (i, float(scores[i]))
        for i in ranked_indices
            
    ]
    max_score = ranked_scores[0][1]
    relevant_documents = [
        _documents[i]
        for i, score in ranked_scores
        if score >= max_score - 0.15
    ]

    return relevant_documents[:top_k]