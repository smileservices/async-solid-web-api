from fastapi import APIRouter
from api.bootstrap import deps
import app_accounts.interface
import app_accounts.serializers

import string
from random import choice, randint

router = APIRouter(tags=["benchmark"])


@router.get("/filter")
async def filter():
    order_should_be = randint(0, 100)
    accounts = await app_accounts.interface.get_accounts_by_order(deps.account_deps, order_should_be)
    return accounts


@router.post("/create")
async def new_account():
    acc = app_accounts.serializers.AccountSerializer(
        id="".join([choice(string.ascii_letters) for _ in range(10)]),
        order=randint(0, 100),
        meta=dict(verified=False, age=choice(range(15, 70)))
    )
    await app_accounts.interface.new_account(deps.account_deps, acc)
    return acc
