from typing import Optional, Union

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from app_accounts.serializers import UserAuthToken

from api.exceptions import NotAuthenticatedException
from core.library.crypto import decode_hmac_jwt, BadTokenException

from api.bootstrap import config_service

import logging

logger = logging.getLogger(__file__)


# we serve the jwt token in http secure cookies
# in order to secure them from client attack vectors
class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise NotAuthenticatedException.status_401
            else:
                return None
        return param


oauth2_scheme_auth_required = OAuth2PasswordBearerWithCookie(
    tokenUrl=config_service.get('AUTH_URL'),
    auto_error=True
)


def user_jwt(token: str = Depends(oauth2_scheme_auth_required)) -> UserAuthToken:
    try:
        if not token:
            raise NotAuthenticatedException.status_401
        secret = config_service.get_secure('JWT_HMAC_SECRET')
        algo = config_service.get_secure('JWT_HMAC_ALGORITHM')
        decoded = decode_hmac_jwt(secret, token, algo=algo)
        user_auth_token = UserAuthToken(**decoded)
        return user_auth_token
    except BadTokenException:
        raise NotAuthenticatedException.status_401
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e
