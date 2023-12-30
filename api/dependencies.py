from dataclasses import dataclass
from app_accounts.dependencies import AccountDependencies


@dataclass
class ApiDependencies:
    account_deps: AccountDependencies
