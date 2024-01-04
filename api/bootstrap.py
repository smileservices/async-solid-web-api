import logging.config

from sqlalchemy.ext.asyncio import create_async_engine

from core.services.config import ConfigService
from core.services.secrets import FileSecret, EnvironSecret
from core.repository import CoreRepository

from app_accounts.dependencies import setup as setup_account_deps
from app_accounts.tables import run_mappers
from app_accounts.dependencies import AccountDependencies

from api.dependencies import ApiDependencies

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)


def setup(config: ConfigService) -> ApiDependencies:
    # we use the freedom of creating the engine here instead
    # of using the component setup function
    async_engine = create_async_engine(
        url=config.get_secure('POSTGRES_URL'),
        pool_size=50,
        max_overflow=350
    )
    acc_repository = CoreRepository(engine=async_engine)
    run_mappers(acc_repository.registry)
    return ApiDependencies(
        account_deps=AccountDependencies(repository=acc_repository)
    )


config_service = ConfigService(
    _secret_manager=FileSecret(env_file_path="api/safe.env"),
    _secure_manager=FileSecret(env_file_path="api/secret.env")
)

deps = setup(config_service)

logger.info("Finished setting up config service and api dependencies")