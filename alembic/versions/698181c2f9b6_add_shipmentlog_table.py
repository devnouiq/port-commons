"""Add ShipmentLog table

Revision ID: 698181c2f9b6
Revises: ef30b9ba308c
Create Date: 2024-11-04 12:52:04.617679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from commons.enums import ScrapeStatus


# revision identifiers, used by Alembic.
revision: str = '698181c2f9b6'
down_revision: Union[str, None] = 'ef30b9ba308c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Use 'create_type=False' to prevent trying to create an existing enum
    scrape_status_enum = postgresql.ENUM('ASSIGNED', 'ACTIVE', 'IN_PROGRESS', 'INELIGIBLE', 'STOPPED', 'FAILED', name='scrapestatus', create_type=False)
    scrape_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'shipment_logs',
        sa.Column('log_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scrape_status', scrape_status_enum, nullable=True),
        sa.Column('scraped_at', sa.DateTime(), nullable=False),
        sa.Column('previous_data', sa.JSON(), nullable=True),
        sa.Column('new_data', sa.JSON(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['shipment_id'], ['shipments.shipment_id'], ),
        sa.PrimaryKeyConstraint('log_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shipment_logs')
    # ### end Alembic commands ###
