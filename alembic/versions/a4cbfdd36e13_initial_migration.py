"""Initial migration

Revision ID: a4cbfdd36e13
Revises: c193425465f0
Create Date: 2024-09-06 15:14:38.316098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4cbfdd36e13'
down_revision: Union[str, None] = 'c193425465f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_auth_tokens_id', table_name='auth_tokens')
    op.drop_table('auth_tokens')
    op.alter_column('shipments', 'terminal_id',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=40),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shipments', 'terminal_id',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
    op.create_table('auth_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='auth_tokens_pkey')
    )
    op.create_index('ix_auth_tokens_id', 'auth_tokens', ['id'], unique=False)
    # ### end Alembic commands ###