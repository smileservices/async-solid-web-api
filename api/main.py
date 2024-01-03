from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from api.benchmark.routes import router as benchmark_router
from api.auth.routes import router as auth_router
from api.bootstrap import deps, config_service

templates = Jinja2Templates(directory="frontend/html")

app = FastAPI()

app.include_router(router=benchmark_router, prefix='/benchmark')
app.include_router(router=auth_router, prefix='/auth')


@app.get("/")
async def homepage(request: Request):
    client_id = config_service.get_secure("TRUSTNET_CLIENT_ID")
    redirect_uri = config_service.get_secure("TRUSTNET_REDIRECT_URL")
    signup_url = f"https://auth.trustnet.app/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid"
    return templates.TemplateResponse(
        "main.html",
        {
            "STATIC_ROUTE": config_service.get("STATIC_ROUTE"),
            "signup_url": signup_url,
            "request": request
        }
    )


# todo verify access jwt and block access only to users

@app.get("/user")
async def user(request: Request):
    return templates.TemplateResponse(
        "user.html",
        {
            "STATIC_ROUTE": config_service.get("STATIC_ROUTE"),
            "request": request
        }
    )
