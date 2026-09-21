import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llmops_control_plane.config import get_settings
from llmops_control_plane.gateway import Gateway
from llmops_control_plane.schemas import GenerateRequest


def log_to_mlflow(average_score: float, case_count: int) -> None:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        return
    try:
        import mlflow
    except ImportError as exc:
        raise SystemExit(
            "MLFLOW_TRACKING_URI is set but mlflow is not installed. "
            "Install with: pip install -e '.[mlops]'"
        ) from exc

    mlflow.set_tracking_uri(tracking_uri)
    with mlflow.start_run(run_name="llmops-golden-eval"):
        mlflow.log_metric("average_score", average_score)
        mlflow.log_metric("case_count", case_count)
        mlflow.log_param("provider", os.getenv("LLM_PROVIDER", "mock"))
        mlflow.log_param("model", os.getenv("LLM_MODEL", "local-model"))


async def run() -> int:
    settings = get_settings()
    gateway = Gateway(settings, ROOT / "data" / "knowledge")
    cases = [
        json.loads(line)
        for line in (ROOT / "evals" / "golden.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    scores = []

    for case in cases:
        response = await gateway.generate(
            GenerateRequest(
                prompt_key=case["prompt_key"],
                variables=case["variables"],
                use_retrieval=True,
            )
        )
        result = gateway.evaluate(
            response.output,
            case.get("expected_keywords", []),
            case.get("required_phrases", []),
        )
        scores.append(result.score)
        print(f"{case['id']}: score={result.score:.4f} passed={result.passed}")

    average = sum(scores) / len(scores) if scores else 0.0
    print(f"average_score={average:.4f} threshold={settings.eval_min_score:.4f}")
    log_to_mlflow(average, len(scores))
    return 0 if average >= settings.eval_min_score and all(
        score >= settings.eval_min_score for score in scores
    ) else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
