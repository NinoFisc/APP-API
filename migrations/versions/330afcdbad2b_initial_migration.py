"""Initial migration

Revision ID: 330afcdbad2b
Revises: 
Create Date: 2024-10-28 09:07:44.868233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '330afcdbad2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraints first
    op.drop_constraint('competitor_association_competitor_id_fkey', 'competitor_association', type_='foreignkey')
    op.drop_constraint('competitor_association_company_id_fkey', 'competitor_association', type_='foreignkey')
    
    # Drop the table
    op.drop_table('company')


def downgrade():
    # Recreate the table
    op.create_table(
        'company',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )
    
    # Recreate foreign key constraints
    op.create_foreign_key('competitor_association_competitor_id_fkey', 'competitor_association', 'competitor', ['competitor_id'], ['id'])
    op.create_foreign_key('competitor_association_company_id_fkey', 'competitor_association', 'company', ['company_id'], ['id'])
