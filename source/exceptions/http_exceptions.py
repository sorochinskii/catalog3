from exceptions.sa_handler_manager import ItemNotFound, NoResultFound
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger

HTTPObjectNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found."
)

HTTPUniqueException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Unique attribute exists."
)


class HttpExceptionsHandler:
    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_instance, traceback):
        match ex_instance:
            case ItemNotFound():
                raise HTTPObjectNotExist
        if ex_instance:
            logger.error(f"Inside HttpExceptionsHandler {ex_instance}")
            raise ex_instance
