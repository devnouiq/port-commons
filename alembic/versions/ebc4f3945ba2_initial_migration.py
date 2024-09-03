"""Initial migration

Revision ID: ebc4f3945ba2
Revises: bb589f6b88a1
Create Date: 2024-09-03 21:50:55.078676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebc4f3945ba2'
down_revision: Union[str, None] = 'bb589f6b88a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('container_status_table', sa.Column('vessel_eta', sa.String(), nullable=True))
    op.drop_column('container_status_table', 'date')
    op.drop_column('container_status_table', 'transit_state')
    op.add_column('shipments', sa.Column('reference_id', sa.String(), nullable=True))
    op.add_column('shipments', sa.Column('company_code', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shipments', 'company_code')
    op.drop_column('shipments', 'reference_id')
    op.add_column('container_status_table', sa.Column('transit_state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('container_status_table', sa.Column('date', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('container_status_table', 'vessel_eta')
    # ### end Alembic commands ###
