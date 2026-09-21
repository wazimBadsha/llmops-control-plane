from prometheus_client import Counter, Histogram

REQUESTS = Counter("llmops_requests_total", "LLM gateway requests", ["provider", "model"])
LATENCY = Histogram("llmops_request_latency_seconds", "Gateway latency", ["provider"])
COST = Counter("llmops_estimated_cost_usd_total", "Estimated request cost", ["provider", "model"])
EVALUATIONS = Counter("llmops_evaluations_total", "Evaluation outcomes", ["status"])
