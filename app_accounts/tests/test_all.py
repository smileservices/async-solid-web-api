import os
import pytest
import logging

from sqlalchemy import orm, create_engine, exc, text, select
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

import app_accounts.interface
from core.repository import CoreRepository

# for sqlalchemy utils
from data_persistence_repository import SqlRepository

from app_accounts.interface import new_account
from app_accounts.serializers import AccountSerializer
from app_accounts import tables
from app_accounts.dependencies import AccountDependencies

"""we test the actual implemetation of the data repository"""

# to use with sqlalchemy_utils
sync_test_db_url = f"postgresql+psycopg2://{os.environ.get('POSTGRES_URL')}/test"

# to use with actual tests
test_db_url = f"postgresql+asyncpg://{os.environ.get('POSTGRES_URL')}/test"

db_engine = create_engine(sync_test_db_url)
async_db_engine = create_async_engine(test_db_url)
async_sess_factory = async_sessionmaker(async_db_engine, class_=AsyncSession)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


@pytest.fixture()
async def test_deps():
    if database_exists(sync_test_db_url):
        drop_database(sync_test_db_url)
    create_database(sync_test_db_url)

    repo = CoreRepository(url=test_db_url)
    await repo.sync_schema()
    tables.run_mappers(repo.registry)

    yield AccountDependencies(
        repository=repo
    )

    # Cleanup code after tests complete
    orm.clear_mappers()
    await async_db_engine.dispose()


@pytest.mark.asyncio
async def test_can_add(test_deps):

    # Obtain the actual AccountDependencies object from the async generator fixture
    async for actual_deps in test_deps:
        acc = AccountSerializer(
            id='somerandomid',
            order=10,
            meta=dict(prop="one")
        )
        await app_accounts.interface.new_account(actual_deps, acc)

    async with async_sess_factory() as s:
        q = await s.execute(text("SELECT * FROM account"))
        res = q.all()
    assert len(res) == 1
    assert res[0][0] == "somerandomid"
    assert res[0][1] == 10
    assert res[0][2] == dict(prop="one")
