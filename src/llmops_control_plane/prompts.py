from pathlib import Path

import yaml

_PROMPT_FILE = Path("prompts/registry.yaml")


def _load_registry() -> dict:
    if not _PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt registry not found: {_PROMPT_FILE}")
    return yaml.safe_load(_PROMPT_FILE.read_text(encoding="utf-8")) or {}


def get_prompt(prompt_key: str, variables: dict[str, str]) -> tuple[str, str]:
    registry = _load_registry().get("prompts", {})
    spec = registry.get(prompt_key)
    if not spec:
        raise KeyError(f"Unknown prompt_key: {prompt_key}")
    template = str(spec["template"])
    prompt = template.format(**variables)
    return str(spec.get("version", "unknown")), prompt
