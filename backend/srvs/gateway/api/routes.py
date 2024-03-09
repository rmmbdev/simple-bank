from starlette.routing import (
    Route,
)

from backend.srvs.gateway.api.endpoints import (
    get_ping,
    post_increment
)

routes = [
    Route(path="/ping/", endpoint=get_ping, methods=["GET"]),
    Route(path="/accounts/{account_id}/increment/", endpoint=post_increment, methods=["POST"]),
]
