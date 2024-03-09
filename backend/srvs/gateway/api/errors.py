from pydantic import (
    ValidationError,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)


async def pydantic_validation_error(request, exc):
    return JSONResponse(content={"details": exc.errors()}, status_code=400)


async def internal_error(request: Request, exc: Exception):
    return JSONResponse(
        content={"details": str(exc)},
        status_code=500,
    )


exception_handlers = {
    Exception: internal_error,
    ValidationError: pydantic_validation_error
}
