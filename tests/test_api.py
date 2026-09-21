from fastapi.testclient import TestClient

from llmops_control_plane.main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate():
    client = TestClient(app)
    response = client.post(
        "/v1/generate",
        json={
            "prompt_key": "support.answer",
            "variables": {"question": "How does LLMOps work?"},
            "use_retrieval": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "mock"
    assert payload["request_id"]
