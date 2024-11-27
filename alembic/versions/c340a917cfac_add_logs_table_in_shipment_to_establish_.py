"""add logs table in shipment to establish connection with shipment_log

Revision ID: c340a917cfac
Revises: a21220b6658d
Create Date: 2024-11-27 12:10:20.525631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'c340a917cfac'
down_revision: Union[str, None] = 'a21220b6658d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add a new column with type UUID
    op.add_column('shipment_logs', sa.Column('log_id_temp', sa.UUID(), nullable=True))

    # Step 2: Populate the new column with generated UUIDs
    op.execute(
        """
        UPDATE shipment_logs
        SET log_id_temp = gen_random_uuid()
        """
    )

    # Step 3: Make the new column non-nullable
    op.alter_column('shipment_logs', 'log_id_temp', nullable=False)

    # Step 4: Drop the old column
    op.drop_column('shipment_logs', 'log_id')

    # Step 5: Rename the new column to `log_id`
    op.alter_column('shipment_logs', 'log_id_temp', new_column_name='log_id')

    # Step 6: Add a unique constraint to the new column
    op.create_unique_constraint('uq_shipment_logs_log_id', 'shipment_logs', ['log_id'])


def downgrade() -> None:
    # Step 1: Add back the old column with type INTEGER
    op.add_column('shipment_logs', sa.Column('log_id_old', sa.Integer(), nullable=True))

    # Step 2: Drop the new UUID column
    op.drop_column('shipment_logs', 'log_id')

    # Step 3: Rename the old column back to `log_id`
    op.alter_column('shipment_logs', 'log_id_old', new_column_name='log_id')
