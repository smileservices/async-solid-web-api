from core.repository import CoreRepository
from core.services.config import ConfigService
from dataclasses import dataclass


@dataclass
class AccountDependencies:
    repository: CoreRepository


def setup(config: ConfigService) -> AccountDependencies:
    repository = CoreRepository(url=config.get('POSTGRES_URL'))
    return AccountDependencies(
        repository=repository
    )