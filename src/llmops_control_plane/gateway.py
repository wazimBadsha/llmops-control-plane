import time
import uuid
from pathlib import Path

from .config import Settings
from .evaluation import evaluate_output
from .metrics import COST, EVALUATIONS, LATENCY, REQUESTS
from .prompts import get_prompt
from .providers import build_provider
from .retrieval import RetrievalIndex
from .schemas import EvaluationResult, GenerateRequest, GenerateResponse
from .tracing import traced


class Gateway:
    def __init__(self, settings: Settings, knowledge_root: Path):
        self.settings = settings
        self.provider = build_provider(settings)
        self.retrieval = RetrievalIndex(knowledge_root)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        started = time.perf_counter()
        request_id = str(uuid.uuid4())
        prompt_version, prompt = get_prompt(request.prompt_key, request.variables)
        retrieved = []
        if request.use_retrieval:
            chunks = self.retrieval.search(prompt, self.settings.retrieval_top_k)
            chunks = [c for c in chunks if c.score > 0]
            context = "\n\n".join(c.text for c in chunks)[: self.settings.max_context_chars]
            retrieved = [c.source for c in chunks]
            if context:
                prompt = f"{prompt}\n\nRetrieved context:\n{context}"
        with traced("llm.generate", request_id=request_id, prompt_version=prompt_version):
            result = await self.provider.generate(prompt)
        latency = time.perf_counter() - started
        estimated_cost = (result.input_tokens_estimate + result.output_tokens_estimate) * 0.000001
        REQUESTS.labels(result.provider, result.model).inc()
        LATENCY.labels(result.provider).observe(latency)
        COST.labels(result.provider, result.model).inc(estimated_cost)
        return GenerateResponse(
            request_id=request_id,
            provider=result.provider,
            model=result.model,
            prompt_key=request.prompt_key,
            output=result.text,
            retrieved_documents=retrieved,
            latency_ms=latency * 1000,
            estimated_cost_usd=estimated_cost,
            input_tokens_estimate=result.input_tokens_estimate,
            output_tokens_estimate=result.output_tokens_estimate,
        )

    def evaluate(self, output: str, expected_keywords: list[str], required_phrases: list[str]) -> EvaluationResult:
        result = evaluate_output(output, expected_keywords, required_phrases, self.settings.eval_min_score)
        EVALUATIONS.labels("pass" if result.passed else "fail").inc()
        return result
