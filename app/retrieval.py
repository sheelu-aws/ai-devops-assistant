
from pathlib import Path
import re

KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "devops_troubleshooting.md"
)

_documents = None


def load_knowledge():
    """Load troubleshooting documents from the knowledge base."""

    if not KNOWLEDGE_FILE.exists():
        return []

    content = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    sections = re.split(r"(?m)^## ", content)[1:]

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def retrieve_knowledge(query: str, top_k: int = 2):
    """Retrieve relevant documents using keyword matching."""

    global _documents

    if not query or not query.strip():
        return []

    if _documents is None:
        _documents = load_knowledge()

    if not _documents:
        return []

    query_words = set(
        re.findall(r"\b[a-zA-Z0-9]+\b", query.lower())
    )

    ranked_documents = []

    for document in _documents:

        document_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                document.lower()
            )
        )

        matching_words = query_words.intersection(
            document_words
        )

        score = len(matching_words)

        if score > 0:
            ranked_documents.append(
                (score, document)
            )

    ranked_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        document
        for score, document in ranked_documents[:top_k]
    ]
