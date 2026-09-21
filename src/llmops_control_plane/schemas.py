from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt_key: str = Field(min_length=1, max_length=120)
    variables: dict[str, str] = Field(default_factory=dict)
    use_retrieval: bool = True


class GenerateResponse(BaseModel):
    request_id: str
    provider: str
    model: str
    prompt_key: str
    output: str
    retrieved_documents: list[str]
    latency_ms: float
    estimated_cost_usd: float
    input_tokens_estimate: int
    output_tokens_estimate: int


class EvaluateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    output: str = Field(min_length=1, max_length=20000)
    expected_keywords: list[str] = Field(default_factory=list)
    required_phrases: list[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    score: float
    passed: bool
    keyword_recall: float
    phrase_recall: float
    checks: dict[str, bool]
