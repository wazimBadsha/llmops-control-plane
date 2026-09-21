# Security

This repository is designed to demonstrate engineering controls, not to certify a production security boundary.

Do not commit:

- API keys or bearer tokens
- cloud credentials
- customer data
- private prompts or proprietary documents
- production endpoints that are not public

For production, place secrets in a managed secret store and enforce identity at the API edge. Treat prompt content and model output as potentially sensitive data and define retention and redaction rules before enabling centralized telemetry.
