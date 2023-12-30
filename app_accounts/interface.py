from app_accounts.dependencies import AccountDependencies
from app_accounts.serializers import AccountSerializer
from app_accounts.models import Account
from dataclasses import asdict


async def new_account(
        deps: AccountDependencies,
        acc: AccountSerializer
) -> AccountSerializer:
    async with deps.repository.start_session() as s:
        instance = Account(
            id=acc.id,
            meta=acc.meta
        )
        await deps.repository.add(s, instance)
        return acc


async def get_account(
        deps: AccountDependencies,
        acc_id: str
) -> AccountSerializer:
    async with deps.repository.start_session() as s:
        acc = await deps.repository.get(s, Account, id=acc_id)
        if not acc:
            raise ValueError("No account exists with this id")
        return AccountSerializer(**asdict(acc))


async def get_accounts(
        deps: AccountDependencies
) -> [AccountSerializer]:
    async with deps.repository.start_session() as s:
        accs = await deps.repository.filter(s, Account)
        return [AccountSerializer(**asdict(acc)) for acc in accs]
