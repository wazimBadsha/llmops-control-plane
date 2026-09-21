# Operations notes

## Local observability

Run:

```bash
docker compose up --build
```

Then use:

- API: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

The sample Grafana JSON is a starting point; production deployments should provision data sources and dashboards explicitly.

## Production extensions

Before exposing the API to untrusted clients, add authentication/authorization, rate limiting, secrets management, encrypted transport, tenant isolation, stronger data redaction, centralized tracing, persistent evaluation storage, and model-specific safety/quality checks.
