from core.services.config import ConfigService
from core.services.secrets import FileSecret, EnvironSecret
from api.dependencies import ApiDependencies
from app_accounts.dependencies import setup as setup_account_deps


def setup(config: ConfigService) -> ApiDependencies:
    return ApiDependencies(
        account_deps=setup_account_deps(config)
    )


config_service = ConfigService(
    _secret_manager=EnvironSecret(),
    _secure_manager=FileSecret(env_file_path="api/.env")
)

deps = setup(config_service)
