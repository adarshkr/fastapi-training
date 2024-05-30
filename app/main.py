import uvicorn
from fastapi import FastAPI, Request
import logging
import os
import time
import asyncio
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError
from fastapi.exceptions import HTTPException

from app.config import config
from app.api import api_router
from app.core.exceptions_handlers import (
    http_exception_handler,
    http_internal_error_handler,
    request_custom_validation_exception_handler,
    request_validation_exception_handler,
    sqlalchemy_error_handler,
)
from app.api.dependencies.deps import JWTAuth

app = FastAPI(title="BE API", version="0.1.0")

log_file_path = os.path.join(os.getcwd(), 'app/logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False) 


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

app.add_exception_handler(Exception, http_internal_error_handler)
app.add_exception_handler(DBAPIError, sqlalchemy_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(ValidationError, request_custom_validation_exception_handler)

@app.middleware("http")
async def http_middleware(request: Request, call_next):
    logging.info(f"{request.method}: {request.url.path}")
    
    start_time = time.time()
    url_path = request.url.path
    
    try:
        response = await asyncio.wait_for(
            call_next(request), timeout=config.REQUEST_TIMEOUT_SECONDS
        )
    except Exception as e:
        raise e
    
    finally:
        process_time = time.time() - start_time
        logging.info(f"Request Complete: {process_time} seconds - {url_path}")
        
    return response


app.include_router(api_router, prefix=config.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=config.DEV_MODE, port=config.PORT)
