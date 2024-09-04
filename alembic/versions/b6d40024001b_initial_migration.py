"""Initial migration

Revision ID: b6d40024001b
Revises: 4f8e95c9e567
Create Date: 2024-09-04 12:40:53.493527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b6d40024001b'
down_revision: Union[str, None] = '4f8e95c9e567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_auth_tokens_id', table_name='auth_tokens')
    op.drop_table('auth_tokens')
    op.alter_column('container_status_table', 'last_updated_availability',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('shipments', sa.Column('run_id', sa.UUID(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shipments', 'run_id')
    op.alter_column('container_status_table', 'last_updated_availability',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_table('auth_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='auth_tokens_pkey')
    )
    op.create_index('ix_auth_tokens_id', 'auth_tokens', ['id'], unique=False)
    # ### end Alembic commands ###
