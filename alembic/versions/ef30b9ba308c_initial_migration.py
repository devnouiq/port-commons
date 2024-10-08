from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef30b9ba308c'
down_revision = '2fb9a9a6d069'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Ensure uuid-ossp extension is enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    
    # Drop the foreign key constraint from container_status_table
    op.drop_constraint('container_status_table_shipment_id_fkey', 'container_status_table', type_='foreignkey')
    
    # Alter 'shipment_id' in 'shipments' table
    op.execute("""
        ALTER TABLE shipments
        ALTER COLUMN shipment_id DROP DEFAULT,
        ALTER COLUMN shipment_id TYPE UUID USING uuid_generate_v5('00000000-0000-0000-0000-000000000000', shipment_id::text);
    """)
    
    # Alter 'shipment_id' in 'container_status_table'
    op.execute("""
        ALTER TABLE container_status_table
        ALTER COLUMN shipment_id DROP DEFAULT,
        ALTER COLUMN shipment_id TYPE UUID USING uuid_generate_v5('00000000-0000-0000-0000-000000000000', shipment_id::text);
    """)
    
    # Recreate the foreign key constraint
    op.create_foreign_key(
        'container_status_table_shipment_id_fkey',
        'container_status_table', 'shipments',
        ['shipment_id'], ['shipment_id'],
        ondelete='CASCADE'
    )
    
    # Continue with other schema changes
    # Create 'auth_tokens' table
    op.create_table('auth_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('terminal_id', sa.String(length=40), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auth_tokens_id'), 'auth_tokens', ['id'], unique=False)
    
    # Add new columns to 'container_status_table'
    op.add_column('container_status_table', sa.Column('vessel_eta', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('last_free_day', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('type_code', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('departed_terminal', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('holds', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('charges', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('demurage', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('line', sa.String(), nullable=True))
    op.add_column('container_status_table', sa.Column('additional_info', sa.JSON(), nullable=True))
    
    # Drop constraints and columns no longer needed
    op.drop_constraint('container_status_table_container_number_key', 'container_status_table', type_='unique')
    op.drop_column('container_status_table', 'last_free_date')
    op.drop_column('container_status_table', 'date')
    op.drop_column('container_status_table', 'last_updated_availability')
    op.drop_column('container_status_table', 'usda_status')
    op.drop_column('container_status_table', 'id')
    op.drop_column('container_status_table', 'vessel_name')
    
    # Add new columns to 'shipments' table
    op.add_column('shipments', sa.Column('vessel_name', sa.String(length=25), nullable=True))
    op.add_column('shipments', sa.Column('reference_id', sa.String(), nullable=True))
    op.add_column('shipments', sa.Column('company_code', sa.String(), nullable=True))
    op.add_column('shipments', sa.Column('vessel_orig_eta', sa.DateTime(), nullable=True))
    op.add_column('shipments', sa.Column('run_id', sa.UUID(), nullable=True))
    
    op.alter_column('shipments', 'terminal_id',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(length=40),
        existing_nullable=True
    )
    op.create_unique_constraint(None, 'shipments', ['shipment_id'])
    op.drop_column('shipments', 'run_date')

def downgrade() -> None:
    # Reverse operations
    op.add_column('shipments', sa.Column('run_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'shipments', type_='unique')
    op.alter_column('shipments', 'terminal_id',
        existing_type=sa.String(length=40),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True
    )
    # Revert 'shipment_id' in 'shipments' table back to INTEGER
    op.execute("""
        ALTER TABLE shipments
        ALTER COLUMN shipment_id TYPE INTEGER USING (shipment_id::text::integer);
    """)
    
    op.drop_column('shipments', 'run_id')
    op.drop_column('shipments', 'vessel_orig_eta')
    op.drop_column('shipments', 'company_code')
    op.drop_column('shipments', 'reference_id')
    op.drop_column('shipments', 'vessel_name')
    
    # Drop the foreign key constraint before altering back
    op.drop_constraint('container_status_table_shipment_id_fkey', 'container_status_table', type_='foreignkey')
    
    # Revert 'shipment_id' in 'container_status_table' back to INTEGER
    op.execute("""
        ALTER TABLE container_status_table
        ALTER COLUMN shipment_id TYPE INTEGER USING (shipment_id::text::integer);
    """)
    
    # Recreate the foreign key constraint
    op.create_foreign_key(
        'container_status_table_shipment_id_fkey',
        'container_status_table', 'shipments',
        ['shipment_id'], ['shipment_id'],
        ondelete='CASCADE'
    )
    
    # Restore dropped columns in 'container_status_table'
    op.add_column('container_status_table', sa.Column('vessel_name', sa.VARCHAR(length=25), autoincrement=False, nullable=True))
    op.add_column('container_status_table', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('container_status_table', sa.Column('usda_status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('container_status_table', sa.Column('last_updated_availability', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('container_status_table', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('container_status_table', sa.Column('last_free_date', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('container_status_table_container_number_key', 'container_status_table', ['container_number'])
    
    # Remove added columns
    op.drop_column('container_status_table', 'additional_info')
    op.drop_column('container_status_table', 'line')
    op.drop_column('container_status_table', 'demurage')
    op.drop_column('container_status_table', 'charges')
    op.drop_column('container_status_table', 'holds')
    op.drop_column('container_status_table', 'departed_terminal')
    op.drop_column('container_status_table', 'type_code')
    op.drop_column('container_status_table', 'last_free_day')
    op.drop_column('container_status_table', 'vessel_eta')
    op.drop_index(op.f('ix_auth_tokens_id'), table_name='auth_tokens')
    op.drop_table('auth_tokens')
