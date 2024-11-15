"""change shipment and container for delete

Revision ID: 476151f91c61
Revises: 698181c2f9b6
Create Date: 2024-11-15 12:55:40.719333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '476151f91c61'
down_revision: Union[str, None] = '698181c2f9b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('container_status_table_shipment_id_fkey', 'container_status_table', type_='foreignkey')
    op.create_foreign_key(None, 'container_status_table', 'shipments', ['shipment_id'], ['shipment_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'container_status_table', type_='foreignkey')
    op.create_foreign_key('container_status_table_shipment_id_fkey', 'container_status_table', 'shipments', ['shipment_id'], ['shipment_id'])
    # ### end Alembic commands ###
