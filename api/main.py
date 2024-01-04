from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from api.benchmark.routes import router as benchmark_router
from api.auth.routes import router as auth_router
from api.auth.utils import user_jwt, UserAuthToken
from api import exceptions

from api.bootstrap import deps, config_service

templates = Jinja2Templates(directory="frontend/html")

app = FastAPI()

app.include_router(router=benchmark_router, prefix='/benchmark')
app.include_router(router=auth_router, prefix='/auth')


@app.get("/")
@exceptions.html_exception
async def homepage(request: Request):
    client_id = config_service.get_secure("TRUSTNET_CLIENT_ID")
    redirect_uri = config_service.get_secure("TRUSTNET_REDIRECT_URL")
    signup_url = f"https://auth.trustnet.app/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid"
    return templates.TemplateResponse(
        "main.html",
        {
            "signup_url": signup_url,
            "request": request
        }
    )


@app.get("/user")
@exceptions.html_exception
async def user(
        request: Request,
        jwt: UserAuthToken = Depends(user_jwt),
):
    return templates.TemplateResponse(
        "user.html",
        {
            "user_id": jwt.user_id,
            "request": request
        }
    )
