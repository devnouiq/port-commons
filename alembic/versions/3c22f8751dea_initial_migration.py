"""Initial migration

Revision ID: 3c22f8751dea
Revises: 7c069ff047fb
Create Date: 2024-08-30 17:16:30.404253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c22f8751dea'
down_revision: Union[str, None] = '7c069ff047fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shipments',
    sa.Column('shipment_id', sa.Integer(), nullable=False),
    sa.Column('container_number', sa.String(length=30), nullable=True),
    sa.Column('master_bol_number', sa.String(length=30), nullable=True),
    sa.Column('house_bol_number', sa.String(length=30), nullable=True),
    sa.Column('run_date', sa.DateTime(), nullable=True),
    sa.Column('voyage_id', sa.Integer(), nullable=True),
    sa.Column('terminal_id', sa.String(length=10), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('scrape_status', sa.Enum('ASSIGNED', 'ACTIVE', 'IN_PROGRESS', 'INELIGIBLE', 'STOPPED', 'FAILED', name='scrapestatus'), nullable=False),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.Column('last_scraped_time', sa.DateTime(), nullable=True),
    sa.Column('next_scrape_time', sa.DateTime(), nullable=True),
    sa.Column('start_scrape_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('shipment_id')
    )
    op.create_table('container_status_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('shipment_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('port', sa.String(), nullable=False),
    sa.Column('terminal', sa.String(), nullable=False),
    sa.Column('container_number', sa.String(), nullable=False),
    sa.Column('available', sa.String(), nullable=False),
    sa.Column('usda_status', sa.String(), nullable=True),
    sa.Column('last_free_date', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('custom_release_status', sa.String(), nullable=True),
    sa.Column('carrier_release_status', sa.String(), nullable=True),
    sa.Column('demurrage_amount', sa.String(), nullable=True),
    sa.Column('vessel_name', sa.String(length=25), nullable=True),
    sa.Column('yard_terminal_release_status', sa.String(), nullable=True),
    sa.Column('last_updated_availability', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.shipment_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('container_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('container_status_table')
    op.drop_table('shipments')
    # ### end Alembic commands ###
