import http
import logging
import traceback

from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError
from sqlalchemy.exc import DBAPIError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.base_response import BaseResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logger.error(
        f"Status Code: {exc.status_code} | Error Type: {type(exc).__name__}  Details: {traceback.format_exc()}"
    )
    return JSONResponse(
        BaseResponse.from_error_str(error=exc.detail).dict(),
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
    )


async def http_internal_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"Status Code: 500 | Error Type: {type(exc).__name__}  Details: {traceback.format_exc()}"
    )
    content = BaseResponse.from_error_str(
        error=http.HTTPStatus(HTTP_500_INTERNAL_SERVER_ERROR).phrase
    ).dict()
    return JSONResponse(content, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(
        f"Status Code: 400 | Error Type: {type(exc).__name__}  Details: {traceback.format_exc()}"
    )

    errors: list = []

    for item in exc.errors():
        errors.append(
            {
                "message": f"{item['loc']} - {item['msg']}",
                "detail": item["ctx"] if "ctx" in item else "",
            }
        )

    content = BaseResponse(errors=errors).dict()
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=content,
    )


async def request_custom_validation_exception_handler(
    _: Request, exc: ValidationError
) -> JSONResponse:
    logger.error(
        f"Status Code: 400 | Error Type: {type(exc).__name__}  Details: {traceback.format_exc()}"
    )
    errors: list = []

    for item in exc.errors():
        errors.append(
            {
                "message": f"{item['loc']} - {item['msg']}",
                "detail": item["ctx"] if "ctx" in item else "",
            }
        )

    content = BaseResponse(errors=errors).dict()

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=content,
    )


async def sqlalchemy_error_handler(_: Request, exc: DBAPIError) -> JSONResponse:
    logger.error(
        f"Status Code: 500 | Error Type: {type(exc).__name__}  Details: {traceback.format_exc()}"
    )
    content = BaseResponse.from_error_str(error=str(exc.orig)).dict()
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
