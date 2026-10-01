from pathlib import Path


def load_documents(knowledge_base_path: str = "knowledge_base"):
    """
    Load Markdown knowledge documents.

    Each document uses a simple metadata header:
    TITLE:
    PUBLISHER:
    URL:
    CATEGORY:
    UPDATED:

    The remaining text is treated as the knowledge content.
    """
    root = Path(knowledge_base_path)
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
            if ":" in line and line.split(":", 1)[0].strip().upper() in {
                "TITLE",
                "PUBLISHER",
                "URL",
                "CATEGORY",
                "UPDATED",
            }:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip()
            else:
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
