from uuid import uuid4

from sqlalchemy import (
    Table,
    Column,
    String,
    Index,
    JSON
)

from core.repository import CoreRepository

from app_accounts.models import Account

metadata = CoreRepository.metadata_obj

account_table = Table(
    "account",
    metadata,
    Column('id', String(256), primary_key=True, nullable=False),
    Column('meta', JSON()),
)

Index('acc_idx', account_table.c.id, unique=True)


def run_mappers(registry):
    registry.map_imperatively(Account, account_table)
