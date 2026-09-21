from fastapi import APIRouter, Depends, Request

from ..gateway import Gateway
from ..schemas import EvaluateRequest

router = APIRouter(prefix="/v1")


def get_gateway(request: Request) -> Gateway:
    return request.app.state.gateway


@router.post("/evaluate")
def evaluate(payload: EvaluateRequest, gateway: Gateway = Depends(get_gateway)):
    return gateway.evaluate(payload.output, payload.expected_keywords, payload.required_phrases)
