from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
)
from starlette.requests import Request
from uuid import uuid4
from backend.srvs.gateway.api.models import (
    GetRequestQueryValidator,
    IncrementBodyValidator,
    IncrementQueryValidator,
    HeaderValidator,
    TransferBodyValidator,
)
from backend.adapters.core import Core
from backend.srvs.gateway.settings import (
    CORE_BASE_URL,
    RABBIT_URL,
    INCREMENT_QUEUE,
    TRANSFER_SMALL_QUEUE,
    TRANSFER_LARGE_QUEUE,
    SMALL_AMOUNT_MAX,
    REDIS_URL,
)
from starlette.exceptions import HTTPException
from backend.libs.rabbit import RabbitAdapter
from backend.libs.redis import RedisAdapter

core_adapter = Core(
    base_url=CORE_BASE_URL,
)

increment_rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=INCREMENT_QUEUE,
)

transfer_small_rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=TRANSFER_SMALL_QUEUE,
)

transfer_large_rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=TRANSFER_LARGE_QUEUE,
)

db = RedisAdapter(
    url=REDIS_URL,
)


def check_token(request):
    headers = dict(request.headers)
    headers_lower_key = {k.lower(): v for k, v in headers.items()}
    header_validated: HeaderValidator = HeaderValidator(**headers_lower_key)
    if not core_adapter.validate_token(header_validated.authorization):
        raise HTTPException(status_code=401, detail="Not authorized, invalid token!")
    return header_validated.authorization


def register_request():
    request_id = str(uuid4())
    db.set(
        name=request_id,
        value="PENDING"
    )
    return request_id


async def get_ping(request):
    return PlainTextResponse("Pong")


async def get_request(request):
    _ = check_token(request)
    path_params_validated: GetRequestQueryValidator = GetRequestQueryValidator(**dict(request.path_params))
    request_id = str(path_params_validated.request_id)

    status = db.get(request_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Request not found!")

    return JSONResponse(
        {
            "request_id": request_id,
            "status": status,
        }
    )


async def post_increment(request: Request):
    token = check_token(request)

    path_params_validated: IncrementQueryValidator = IncrementQueryValidator(**dict(request.path_params))
    account_id = str(path_params_validated.account_id)

    body = await request.json()
    body_validated: IncrementBodyValidator = IncrementBodyValidator(**body)

    request_id = register_request()

    increment_rabbit.publish(
        {
            "request_id": request_id,
            "account_id": account_id,
            "amount": body_validated.amount,
            "token": token,
        }
    )

    return JSONResponse(
        {
            "request_id": request_id,
        }
    )


async def post_transfer(request: Request):
    token = check_token(request)

    body = await request.json()
    body_validated: TransferBodyValidator = TransferBodyValidator(**body)
    source = str(body_validated.source)
    destination = str(body_validated.destination)
    amount = body_validated.amount

    request_id = register_request()

    if amount < SMALL_AMOUNT_MAX:
        transfer_small_rabbit.publish(
            {
                "request_id": request_id,
                "source": source,
                "destination": destination,
                "amount": amount,
                "token": token,
            }
        )
    else:
        transfer_large_rabbit.publish(
            {
                "request_id": request_id,
                "source": source,
                "destination": destination,
                "amount": amount,
                "token": token,
            }
        )

    return JSONResponse(
        {
            "request_id": request_id,
        }
    )
