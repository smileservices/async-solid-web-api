from datetime import datetime, timedelta
from jose import JWTError, jwt, exceptions, jwk
from jose.backends import RSAKey

from jose.constants import ALGORITHMS
from typing import Callable, Optional
from jose.utils import base64url_decode
import json
import jwt as pyjwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60

jwt_validation_options = {
    'verify_signature': True,
    'verify_iat': True,
    'verify_exp': True,
    'verify_nbf': True,
    'verify_iss': True,
    'verify_at_hash': True,
    'verify_aud': False,
    'verify_sub': False,
    'verify_jti': False,
    'require_aud': False,
    'require_iat': False,
    'require_exp': False,
    'require_nbf': False,
    'require_iss': False,
    'require_sub': False,
    'require_jti': False,
    'require_at_hash': False,
    'leeway': 0,
}


class BadTokenException(Exception):
    pass


def encode_hmac_jwt(secret, data: dict, algo: str = ALGORITHMS.HS256, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=300)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algo)
    return encoded_jwt


def decode_hmac_jwt(secret, token, verify_callback: Optional[Callable] = None, algo: str = ALGORITHMS.HS256) -> dict:
    try:
        decoded = jwt.decode(token, secret, algorithms=[algo])
    except JWTError as e:
        raise BadTokenException('Could not decode')
    if verify_callback and not verify_callback(decoded):
        raise BadTokenException('JWT content verification fail')
    return decoded


def decode_signed_jwt(jwk_response: dict, token: str, iss: str) -> dict:
    if 'keys' not in jwk_response or not jwk_response['keys']:
        raise ValueError("No keys found in JWKS response")
    key_info = jwk_response['keys'][0]
    algorithm = key_info.get('alg')
    if not algorithm:
        raise ValueError("Algorithm not found in JWKS response")
    key = jwk.construct(key_info, algorithm)
    try:
        decoded = jwt.decode(token, key.to_pem(), issuer=iss, options=jwt_validation_options, algorithms=[algorithm])
    except exceptions.JWTClaimsError as e:
        raise BadTokenException(f'Token invalid: {str(e)}')
    except exceptions.JWTError as e:
        raise BadTokenException(f'Could not decode: {str(e)}')
    return decoded
