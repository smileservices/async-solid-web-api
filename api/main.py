from fastapi import FastAPI
from api.bootstrap import deps
import app_accounts.interface
import app_accounts.serializers
import string
from random import choice

app = FastAPI()


@app.get("/")
async def all_accounts():
    accounts = await app_accounts.interface.get_accounts(deps.account_deps)
    return accounts


@app.post("/")
async def new_account():
    acc = app_accounts.serializers.AccountSerializer(
        id="".join([choice(string.ascii_letters) for _ in range(10)]),
        meta=dict(verified=False, age=choice(range(15, 70)))
    )
    await app_accounts.interface.new_account(deps.account_deps, acc)
    return acc
