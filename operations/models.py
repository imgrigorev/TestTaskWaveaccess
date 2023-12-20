from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from datetime import datetime

metadata = MetaData()


task = Table(
    'task',
    metadata,
Column("number", primary_key=True, index=True),
    Column("username", String, nullable=False),
    Column("priority", String, nullable=False),
    Column("status", String, nullable=False),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("executor", String, nullable=False),
    Column("creator", String, nullable=False),
    Column("created_at",  TIMESTAMP, default=datetime.utcnow),
    Column("updated_at",  TIMESTAMP, default=datetime.utcnow),
    Column("type", String, nullable=False),
    Column("blocking_tasks", String, nullable=False),
)