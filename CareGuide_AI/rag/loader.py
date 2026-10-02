from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB_PATH = PROJECT_ROOT / "knowledge_base"


def load_documents(knowledge_base_path=None):
    """
    Load Markdown files from the project knowledge_base directory.

    The path is resolved from this Python file, not from the process
    working directory. This makes the RAG system reliable on Streamlit Cloud.
    """
    root = Path(knowledge_base_path) if knowledge_base_path else DEFAULT_KB_PATH
    root = root.resolve()

    documents = []

    if not root.exists():
        return documents

    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        metadata = {
            "title": path.stem.replace("_", " ").title(),
            "publisher": "Unknown",
            "url": "",
            "category": "general",
            "updated": "",
        }

        content_lines = []

        for line in text.splitlines():
            stripped = line.strip()

            if ":" in stripped:
                key, value = stripped.split(":", 1)
                key = key.strip().upper()

                if key in {"TITLE", "PUBLISHER", "URL", "CATEGORY", "UPDATED"}:
                    metadata[key.lower()] = value.strip()
                    continue

            content_lines.append(line)

        content = "\n".join(content_lines).strip()

        if content:
            documents.append(
                {
                    "content": content,
                    "metadata": metadata,
                    "path": str(path),
                }
            )

    return documents
