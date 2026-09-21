from contextlib import contextmanager
import logging
import time

logger = logging.getLogger(__name__)


@contextmanager
def traced(operation: str, **fields: object):
    started = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info("trace operation=%s latency_ms=%.2f fields=%s", operation, elapsed_ms, fields)
