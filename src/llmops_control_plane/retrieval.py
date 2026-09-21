from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    text: str
    score: float


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]{3,}", text.lower()))


class RetrievalIndex:
    """Transparent lexical baseline for RAG.

    The implementation intentionally favors explainability over sophistication so a
    reader can inspect exactly why a chunk was returned. It is a swap point for a
    vector database/embedding model later.
    """

    def __init__(self, root: Path):
        self.chunks: list[RetrievedChunk] = []
        for path in sorted(root.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for block in [part.strip() for part in text.split("\n\n") if part.strip()]:
                self.chunks.append(RetrievedChunk(path.name, block, 0.0))

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        q = _tokens(query)
        scored: list[RetrievedChunk] = []
        for chunk in self.chunks:
            c = _tokens(chunk.text)
            score = len(q & c) / max(1, len(q))
            scored.append(RetrievedChunk(chunk.source, chunk.text, score))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]
