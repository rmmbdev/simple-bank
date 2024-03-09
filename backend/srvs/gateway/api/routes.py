from starlette.routing import (
    Route,
)

from backend.srvs.gateway.api.endpoints import (
    get_ping,
    get_request,
    post_increment,
)

routes = [
    Route(path="/ping/", endpoint=get_ping, methods=["GET"]),
    Route(path="/requests/{request_id}/", endpoint=get_request, methods=["GET"]),
    Route(path="/accounts/{account_id}/increment/", endpoint=post_increment, methods=["POST"]),
]
