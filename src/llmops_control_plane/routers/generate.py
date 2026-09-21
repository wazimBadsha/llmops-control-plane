from fastapi import APIRouter, Depends, Header, HTTPException, Request

from ..config import get_settings
from ..gateway import Gateway
from ..schemas import GenerateRequest
from ..security import authorize

router = APIRouter(prefix="/v1")


def get_gateway(request: Request) -> Gateway:
    return request.app.state.gateway


@router.post("/generate")
async def generate(
    payload: GenerateRequest,
    gateway: Gateway = Depends(get_gateway),
    x_api_key: str | None = Header(default=None),
):
    settings = get_settings()
    if not authorize(x_api_key, settings.api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await gateway.generate(payload)
