import re
from secrets import compare_digest

_SECRET_PATTERNS = [
    re.compile(r"(?i)sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{16,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*[^\s,;]{12,}"),
]


def authorize(provided: str | None, expected: str | None) -> bool:
    if not expected:
        return True
    return bool(provided) and compare_digest(provided, expected)


def redact(value: str) -> str:
    redacted = value
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
