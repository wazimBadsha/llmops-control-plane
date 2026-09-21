from dataclasses import dataclass

import httpx

from .config import Settings


@dataclass
class ProviderResult:
    provider: str
    model: str
    text: str
    input_tokens_estimate: int
    output_tokens_estimate: int


class MockProvider:
    name = "mock"
    model = "deterministic-v1"

    async def generate(self, prompt: str) -> ProviderResult:
        lower = prompt.lower()
        if "retrieval" in lower and "inspectable" in lower:
            answer = (
                "A transparent lexical baseline makes retrieval more explainable because "
                "the selected document can be inspected directly."
            )
        else:
            answer = (
                "LLMOps turns model output into an observable, testable software artifact: "
                "version the prompt, evaluate the output, measure latency/cost, and promote "
                "changes through CI before deployment."
            )
        input_tokens = max(1, len(prompt.split()))
        output_tokens = len(answer.split())
        return ProviderResult(self.name, self.model, answer, input_tokens, output_tokens)


class OpenAICompatibleProvider:
    name = "openai_compatible"

    def __init__(self, settings: Settings):
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.timeout = settings.llm_timeout_seconds

    async def generate(self, prompt: str) -> ProviderResult:
        headers = {"content-type": "application/json"}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            body = response.json()
        text = body["choices"][0]["message"]["content"]
        usage = body.get("usage", {})
        return ProviderResult(
            self.name,
            self.model,
            text,
            int(usage.get("prompt_tokens", max(1, len(prompt.split())))),
            int(usage.get("completion_tokens", max(1, len(text.split())))),
        )


def build_provider(settings: Settings):
    if settings.llm_provider == "openai_compatible":
        return OpenAICompatibleProvider(settings)
    return MockProvider()
