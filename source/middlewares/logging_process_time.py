import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette.routing import Match


async def x_process_time_header(request: Request, call_next):

    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.bind(
            url=request.url,
            method=request.method,
            status_code=response.status_code,
            elapsed=process_time,
        ).debug(
            "incoming {method} request {url} response status {status_code}",
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response
