from pathlib import Path

from fastapi import FastAPI
from prometheus_client import make_asgi_app

from .config import get_settings
from .gateway import Gateway
from .routers import evaluate, generate, health

settings = get_settings()
app = FastAPI(title="LLMOps Control Plane", version="0.1.0")
app.state.gateway = Gateway(settings, Path("data/knowledge"))
app.include_router(health.router)
app.include_router(generate.router)
app.include_router(evaluate.router)
app.mount("/metrics", make_asgi_app())
