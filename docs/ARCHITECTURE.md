# Architecture

## Runtime path

1. The client submits a `prompt_key` and variables.
2. The gateway loads the versioned prompt from the registry.
3. Optional retrieval searches the local knowledge corpus.
4. The provider adapter sends the final prompt to a deterministic mock or an OpenAI-compatible inference endpoint.
5. The gateway returns the output plus operational metadata.
6. Prometheus counters record request count, latency, tokens, estimated cost, and evaluation results.

## Why the provider boundary matters

The model integration is deliberately isolated behind `ProviderResult` and `build_provider()`. A production extension can add:

- hosted provider A/B routing
- a self-hosted vLLM/Ollama provider
- a safety classifier before generation
- retry/backoff policies
- circuit breakers
- region-aware routing
- tenant-specific model policies

The rest of the application should not care which provider executes the request.

## Why the retrieval baseline is lexical

A vector database is useful, but a showcase should make the control loop obvious. The lexical index is deterministic, dependency-light, and inspectable. Swapping in embeddings later becomes an explicit architecture change rather than hidden magic.

## CI quality gate

The golden dataset is executed by `scripts/evaluate.py`. The score must meet the configured threshold for every case. The same command can be used from CI, a release pipeline, or a deployment promotion workflow.
