"""Added required tables

Revision ID: 8f17cbd48f65
Revises: 207df6c91674
Create Date: 2023-12-19 23:17:11.560012

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8f17cbd48f65'
down_revision: Union[str, None] = '207df6c91674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_user_tokens_id'), 'user_tokens', ['id'], unique=False)
    op.drop_index('ix_task_number', table_name='task')
    op.drop_table('task')
    op.drop_index('ix_tokens_token', table_name='tokens')
    op.drop_table('tokens')
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('password', sqlalchemy_utils.types.password.PasswordType(max_length=1094), nullable=True))
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               existing_nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=40),
               type_=sqlalchemy_utils.types.email.EmailType(length=50),
               nullable=False)
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.alter_column('users', 'email',
               existing_type=sqlalchemy_utils.types.email.EmailType(length=50),
               type_=sa.VARCHAR(length=40),
               nullable=True)
    op.alter_column('users', 'name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.drop_column('users', 'password')
    op.drop_column('users', 'role')
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', postgresql.UUID(), server_default=sa.text("'f2ce07d8-b911-428f-953b-be3ea5495141'::uuid"), autoincrement=False, nullable=False),
    sa.Column('expires', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tokens_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey')
    )
    op.create_index('ix_tokens_token', 'tokens', ['token'], unique=False)
    op.create_table('task',
    sa.Column('number', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('priority', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('executor', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('creator', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('blocking_tasks', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('number', name='task_pkey')
    )
    op.create_index('ix_task_number', 'task', ['number'], unique=False)
    op.drop_index(op.f('ix_user_tokens_id'), table_name='user_tokens')
    op.drop_table('user_tokens')
    # ### end Alembic commands ###
