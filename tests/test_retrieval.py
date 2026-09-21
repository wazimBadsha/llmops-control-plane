from pathlib import Path

from llmops_control_plane.retrieval import RetrievalIndex


def test_retrieval_returns_matching_source():
    index = RetrievalIndex(Path("data/knowledge"))
    results = index.search("Why should retrieval be inspectable?", 2)
    assert results
    assert results[0].source == "rag.md"
    assert results[0].score > 0
