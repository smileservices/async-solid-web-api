from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import aiohttp
from time import time

from core.library.crypto import encode_hmac_jwt, decode_signed_jwt

from app_accounts import interface as acc_interface
from app_accounts.serializers import AccountSerializer, UserAuthToken

from api.bootstrap import deps, config_service

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="frontend/html")


@router.get("/oidc")
async def handle_code(
        request: Request,
        code: str,
        state: None | str = None
):
    data = {
        "grant_type": "code",
        "client_id": config_service.get_secure('TRUSTNET_CLIENT_ID'),
        "client_secret": config_service.get_secure('TRUSTNET_CLIENT_SECRET'),
        "redirect_uri": config_service.get_secure('TRUSTNET_REDIRECT_URL'),
        "code": code,
        "state": state if state else None
    }
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:

        # this should be cached
        async with session.get(config_service.get_secure("TRUSTNET_OPENID_CONFIG_URL")) as config_response:
            provider_config = await config_response.json()

    async with aiohttp.ClientSession() as session:

        # get the access token
        async with session.post(provider_config["token_endpoint"], json=data, headers=headers) as token_resp:
            tokens = await token_resp.json()
            if token_resp.status != 200:
                return templates.TemplateResponse(
                    "error.html",
                    {
                        "provider_config": provider_config,
                        "request": request, "error": tokens["detail"]
                    }
                )

        # decode id token and check signature
        async with session.get(provider_config["jwks_uri"]) as jwks_res:
            jwks_res_dict = await jwks_res.json()
            decoded_id_token = decode_signed_jwt(jwks_res_dict, tokens['id_token'], iss="trustnet.app")

        # check if account already exists
        try:
            account = await acc_interface.get_account(deps.account_deps, acc_id=decoded_id_token['sub'])
        except ValueError:
            # get userinfo from oidc provider
            auth_header = f'{tokens["token_type"]} {tokens["access_token"]}'
            async with session.get(
                    provider_config["userinfo_endpoint"],
                    headers={"authorization": auth_header}
            ) as user_info_req:
                user_info = await user_info_req.json()
                acc_ser = AccountSerializer(
                    id=decoded_id_token['sub'],
                    order=1,
                    meta=user_info
                )
                account = await acc_interface.new_account(deps.account_deps, acc_ser)

    # create response
    response = RedirectResponse(
        url="/user",
    )
    # create jwt
    token = UserAuthToken(
        user_id=account.id,
        auth_time=time(),
        exp=60
    )
    secret = config_service.get_secure('JWT_HMAC_SECRET')
    algo = config_service.get_secure('JWT_HMAC_ALGORITHM')
    token = encode_hmac_jwt(secret, token.__dict__, algo=algo)
    response.set_cookie(
        key='access_token',
        value=f"Bearer {token}",
        secure=True,
        httponly=True,
        samesite="lax",
        domain=f'{config_service.get("DOMAIN")}'
    )
    return response
