from core.repository import CoreRepository
from core.services.config import ConfigService
from dataclasses import dataclass
from app_accounts.tables import run_mappers


@dataclass
class AccountDependencies:
    repository: CoreRepository


def setup(config: ConfigService) -> AccountDependencies:
    repository = CoreRepository(url=config.get('POSTGRES_URL'))
    run_mappers(repository.registry)
    return AccountDependencies(
        repository=repository
    )