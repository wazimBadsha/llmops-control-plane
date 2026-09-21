# LLMOps Control Plane

A production-minded, local-first reference implementation for building and operating LLM applications with measurable quality.

This showcase combines a model gateway, versioned prompts, transparent RAG retrieval, deterministic evaluation gates, telemetry, cost/latency metrics, Docker, Kubernetes manifests, and CI.

LLM Gateway → Prompt Registry → RAG → Model Provider → Evaluation Gate → Metrics → Grafana → CI/CD


## Why this project exists

Most LLM demos stop at:

```text
prompt -> model -> answer
```

Production AI systems need a control loop:

```text
Client
  |
  v
LLM Gateway
  |
  +--> Prompt Registry
  |
  +--> Retrieval
  |
  v
Model Provider
  |
  v
Output + operational metadata
  |
  +--> Prometheus / Grafana
  +--> Evaluation gate
  +--> optional MLflow
  |
  v
CI -> release -> deploy -> monitor
```

The goal is to demonstrate the engineering around the model, not merely model invocation.

## What it demonstrates

- **LLM engineering:** model-agnostic generation API, provider abstraction, structured contracts.
- **MLOps:** golden datasets, repeatable evaluation, regression thresholds and release gates.
- **AI/ML:** transparent retrieval baseline that can later be replaced with embeddings/vector search.
- **Platform engineering:** health checks, metrics, structured tracing hooks, Docker, Kubernetes and CI.
- **Operational thinking:** latency, token estimates, cost estimates, request IDs and safety boundaries.

## Repository map

```text
src/llmops_control_plane/  API, gateway, providers, retrieval, evaluation, telemetry
prompts/                   versioned prompt registry
models/                    model/provider registry
evals/                     golden evaluation set
data/knowledge/            sample RAG corpus
scripts/                   evaluation runner
tests/                     API, evaluation and retrieval tests
observability/             Prometheus configuration
grafana/                   dashboard JSON
k8s/                       Kubernetes examples
docs/                      architecture and operations
medium/                    publish-ready Medium article
.github/workflows/         CI quality gate
```

## Quick start

### Local deterministic mode

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
uvicorn llmops_control_plane.main:app --reload
```

API:

`http://127.0.0.1:8000/docs`

Generate:

```bash
curl -s http://127.0.0.1:8000/v1/generate \
  -H 'content-type: application/json' \
  -d '{
    "prompt_key": "support.answer",
    "variables": {"question": "How does the evaluation gate work?"},
    "use_retrieval": true
  }'
```

Run tests:

```bash
pytest -q
```

Run the quality gate:

```bash
python scripts/evaluate.py
```

## OpenAI-compatible inference

The provider layer supports any inference server exposing an OpenAI-compatible chat-completions contract.

Example:

```dotenv
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_API_KEY=replace-me
LLM_MODEL=your-model
```

No real credentials belong in this repository.

## MLOps control loop

```text
Prompt / data change
       |
       v
Golden evaluation set
       |
       v
Deterministic quality checks
       |
   +---+---+
   |       |
 pass     fail
   |       |
   v       v
release   block
   |
   v
metrics + traces
   |
   v
operate -> learn -> improve
```

The important idea is to treat model output quality as a software quality signal. Prompt changes become reviewable, testable and promotable.

## Observability

The gateway exposes Prometheus metrics for:

- request count
- latency
- estimated cost
- evaluation status

The local Compose stack includes:

- API on port 8000
- Prometheus on port 9090
- Grafana on port 3000

```bash
docker compose up --build
```

## Kubernetes

Examples are under `k8s/`.

They intentionally use environment-neutral placeholders. Replace the image registry, ingress host and secret wiring before deploying.

## Security

This is a public engineering showcase, not a production security certification.

Before exposing it to untrusted clients, add:

- centralized identity and authorization
- rate limiting
- managed secrets
- TLS
- tenant isolation
- stronger prompt/output redaction
- audit logging
- data retention controls
- model-specific safety evaluations

See [SECURITY.md](SECURITY.md).

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Operations](docs/OPERATIONS.md)
- [Public showcase checklist](docs/SHOWCASE_CHECKLIST.md)
- [Medium article](medium/medium-post.md)
- [Contributing](CONTRIBUTING.md)

## Positioning

This repository is an engineering showcase for **MLOps + AI/ML + LLM systems engineering**.

The emphasis is deliberately on the bridge between application engineering and reliable model operations:

**version -> test -> evaluate -> observe -> release -> monitor -> improve**

## License

MIT — Copyright (c) 2026 Badhusha K
