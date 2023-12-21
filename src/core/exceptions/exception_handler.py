from datetime import datetime
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from src.core.exceptions.exception import DatabaseException, NotFoundException
from starlette.responses import JSONResponse

from src.schemas.error import Error


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = {}
    for validation_error in exc.errors():
        loc, msg = validation_error["loc"], validation_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        invalid_data = ".".join(filtered_loc)
        error_message[invalid_data] = msg
    # Join the individual error messages
    error_message_data = ", ".join(" ".join([key, str(value)]) for key, value in error_message.items())
    error_message_data = error_message_data.replace("__root__", "").strip()
    error_response = Error(
        error="Invalid request",
        message=error_message_data,
        path=str(request.url),
        timestamp=str(datetime.now()),
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    return JSONResponse(content=jsonable_encoder(error_response), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def resource_not_found_exception_handler(request: Request, exc: NotFoundException):
    error_response = Error(
        error=exc.error,
        message=exc.message,
        path=str(request.url),
        timestamp=str(datetime.now()),
        status=status.HTTP_404_NOT_FOUND,
    )
    return JSONResponse(content=jsonable_encoder(error_response), status_code=status.HTTP_404_NOT_FOUND)


async def database_exception_handler(request: Request, exc: DatabaseException):
    error_response = Error(
        error=exc.error,
        message=exc.message,
        path=str(request.url),
        timestamp=str(datetime.now()),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return JSONResponse(content=jsonable_encoder(error_response), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
