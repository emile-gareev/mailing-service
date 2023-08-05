from fastapi import Request, Response
from logging import getLogger
from typing import Callable


logger = getLogger(__name__)


async def exception_handle(request: Request, call_next: Callable) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        route = f'{request.method} {request.url}'
        info = f'Exception {e.__class__}: {e}'
        logger.error(f'{route}\n{info}')
        return Response(content=info, status_code=500)
