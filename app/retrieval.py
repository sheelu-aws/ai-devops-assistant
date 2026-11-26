
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


def retrieve_knowledge(query: str, top_k: int = 4):
    """Retrieve relevant documents using weighted keyword matching."""

    global _documents

    if not query or not query.strip():
        return []

    if _documents is None:
        _documents = load_knowledge()

    if not _documents:
        return []

    query_lower = query.lower()

    query_words = set(
        re.findall(r"\b[a-zA-Z0-9]+\b", query_lower)
    )

    # Important DevOps symptoms and their troubleshooting topics
    priority_signals = {
        "http 502": [
            "502",
            "bad gateway",
            "503",
            "service unavailable",
            "ingress"
        ],
        "high cpu": [
            "cpu",
            "high load",
            "processor"
        ],
        "memory issues": [
            "oomkilled",
            "oom",
            "out of memory",
            "memory leak",
            "memory"
        ],
        "imagepullbackoff": [
            "imagepullbackoff",
            "errimagepull",
            "image pull",
            "registry"
        ]
    }

    ranked_documents = []

    for document in _documents:

        document_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                document.lower()
            )
        )

        # Calculate normal keyword matching score
        matching_words = query_words.intersection(
            document_words
        )

        score = len(matching_words)

        # Give additional weight to important DevOps symptoms
        document_title = document.splitlines()[0].lower()

        for topic, signals in priority_signals.items():

            if topic in document_title:

                for signal in signals:

                    if signal in query_lower:
                        score += 5

        if score > 0:
            ranked_documents.append(
                (score, document)
            )

    # Sort documents by relevance score
    ranked_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        document
        for score, document in ranked_documents[:top_k]
    ]
