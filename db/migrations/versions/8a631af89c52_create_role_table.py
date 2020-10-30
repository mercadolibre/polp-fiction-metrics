"""empty message
Revision ID: 8a631af89c52
Revises: c3e75010b1aa
Create Date: 2020-07-20 14:12:52.293099
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8a631af89c52'
down_revision = 'c3e75010b1aa'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('role',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('name', sa.String(255)),
                    sa.Column('arn', sa.String(255), nullable=False),
                    sa.Column('last_used', sa.DateTime()),
                    sa.Column('last_used_region', sa.String(255)),
                    sa.Column('foreign', sa.Boolean(), nullable=False),
                    sa.Column('ext_entity_compliance', sa.Boolean()),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('inline_count', sa.Integer()),
                    sa.ForeignKeyConstraint(('account_id',), ['account.id']),
                    sa.UniqueConstraint('arn', 'account_id'),
                    sa.Column('job_uuid', sa.String(255), nullable=False),
                    sa.Column('create_date', sa.DateTime()),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False)
                    )

def downgrade():
    op.drop_table('role')
