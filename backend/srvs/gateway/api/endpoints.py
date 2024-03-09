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
from backend.adapters.core import Core
from backend.srvs.gateway.settings import (
    CORE_BASE_URL,
    RABBIT_URL,
    INCREMENT_QUEUE,
    TRANSFER_QUEUE,

)
from starlette.exceptions import HTTPException
from backend.libs.rabbit import RabbitAdapter

core_adapter = Core(
    base_url=CORE_BASE_URL,
)

increment_rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=INCREMENT_QUEUE,
)

transfer_rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=TRANSFER_QUEUE,
)


async def get_ping(request):
    return PlainTextResponse("Pong")


async def post_increment(request: Request):
    path_params_validated = IncrementQueryValidator(**dict(request.path_params))

    body = await request.json()
    body_validated = IncrementBodyValidator(**body)

    headers = dict(request.headers)
    headers_lower_key = {k.lower(): v for k, v in headers.items()}
    header_validated = HeaderValidator(**headers_lower_key)

    if not core_adapter.validate_token(header_validated.authorization):
        raise HTTPException(status_code=401, detail="Not authorized, invalid token!")
    data = {
        "msg": "done"
    }

    return JSONResponse(data)
