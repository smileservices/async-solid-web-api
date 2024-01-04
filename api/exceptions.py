import logging
from functools import wraps
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

from api.bootstrap import config_service

templates = Jinja2Templates(directory="frontend/html")


class OAuthException(Exception):

    def __str__(self):
        return f"OAuth: {super().__str__()}"


class TokenException(OAuthException):

    def __str__(self):
        return f"Token: {super().__str__()}"


class HttpExceptionModel(BaseModel):
    detail: str


class NotAuthenticatedException(Exception):
    status_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def api_exception(fn):
    """
    A decorator that catches exceptions thrown by the decorated function,
    logs the exception and raises an HTTPException with a status code of 500 and detail "Something went wrong".

    :param fn: The function to be decorated.
    :return: A new function that wraps the original function and catches exceptions.
    """

    @wraps(fn)
    async def _wrapped(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except NotAuthenticatedException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger = logging.getLogger(fn.__module__)
            logger.error(f"error: {e}", exc_info=config_service.get("EXC_INFO"))
            raise HTTPException(
                status_code=500,
                detail=str(e) if config_service.get("DEV") else "Something went terribly wrong"
            )

    return _wrapped


def html_exception(fn):
    """
    A decorator that catches exceptions thrown by the decorated function,
    logs the exception and returns the html error page with status code of 500 and the error detail.

    :param fn: The function to be decorated.
    :return: A new function that wraps the original function and catches exceptions.
    """

    @wraps(fn)
    async def _wrapped(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except NotAuthenticatedException as e:
            return RedirectResponse(url=config_service.get("AUTH_URL"))
        except HTTPException as e:
            return templates.TemplateResponse(
                status_code=e.status_code,
                name="error.html", context={
                    "config": config_service,
                    "request": kwargs.get("request"),
                    "error_detail": e.detail
                },
            )
        except Exception as e:
            logger = logging.getLogger(fn.__module__)
            logger.error(f"error: {e}", exc_info=config_service.get("EXC_INFO"))
            return templates.TemplateResponse(
                status_code=500,
                name="error.html", context={
                    "config": config_service,
                    "request": kwargs.get("request"),
                    "error_detail": str(e) if config_service.get("DEV") else "Something went terribly wrong"
                },
            )

    return _wrapped
