"""Initial migration

Revision ID: b040818708e8
Revises: e459a449bb75
Create Date: 2024-08-30 23:05:16.427211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b040818708e8'
down_revision: Union[str, None] = 'e459a449bb75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('container_status_table', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('container_status_table', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    # ### end Alembic commands ###
