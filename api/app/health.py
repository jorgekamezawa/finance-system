from typing import Annotated, Protocol

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse


class ReadinessCheck(Protocol):
    """Boundary the route depends on: tells whether the database is reachable."""

    async def database_is_ready(self) -> bool: ...


def get_readiness_check(request: Request) -> ReadinessCheck:
    readiness_check: ReadinessCheck = request.app.state.readiness_check
    return readiness_check


router = APIRouter()


@router.get("/health")
async def health(
    readiness: Annotated[ReadinessCheck, Depends(get_readiness_check)],
) -> Response:
    if await readiness.database_is_ready():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "ok", "checks": {"db": "ok"}},
        )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "degraded", "checks": {"db": "down"}},
    )
