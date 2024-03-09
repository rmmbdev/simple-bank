from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
)
from starlette.requests import Request

from backend.srvs.gateway.api.models import (
    IncrementBodyValidator,
    IncrementQueryValidator,
    HeaderValidator,
)


async def get_ping(request):
    return PlainTextResponse("Pong")


async def post_increment(request: Request):
    path_params_validated = IncrementQueryValidator(**dict(request.path_params))

    body = await request.json()
    body_validated = IncrementBodyValidator(**body)

    header_validated = HeaderValidator(**dict(request.headers))

    data = {
        "msg": "done"
    }

    return JSONResponse(data)
