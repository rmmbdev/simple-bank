import uvicorn
from starlette.applications import (
    Starlette,
)

from backend.srvs.gateway.api.errors import (
    exception_handlers,
)
from backend.srvs.gateway.api.routes import (
    routes,
)
from backend.srvs.gateway.settings import (
    DEBUG,
    PORT,
)

app = Starlette(
    debug=DEBUG,
    routes=routes,
    exception_handlers=exception_handlers,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
