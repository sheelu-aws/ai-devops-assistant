from pathlib import Path
import re

KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "devops_troubleshooting.md"
)


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return []

    content = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", content)[1:]

    documents = []

    for section in sections:
        section = section.strip()
        if section:
            documents.append(section)

    return documents


def retrieve_knowledge(query: str, top_k: int = 2):
    documents = load_knowledge()
    query_words = set(re.findall(r"\b[a-z0-9]+\b", query.lower()))

    scored_documents = []

    for document in documents:
        document_words = set(
            re.findall(r"\b[a-z0-9]+\b", document.lower())
        )
        score = len(query_words & document_words)

        if score > 0:
            scored_documents.append((score, document))

    scored_documents.sort(key=lambda item: item[0], reverse=True)

    return [
        document
        for score, document in scored_documents[:top_k]
    ]
