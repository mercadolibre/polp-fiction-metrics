
"""empty message
Revision ID: 18c3b62838e8
Revises: 589d44582d97
Create Date: 2020-07-20 15:44:22.011079
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '18c3b62838e8'
down_revision = '589d44582d97'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('policy',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('arn', sa.String(255), nullable=False),
                    sa.Column('name', sa.String(255), nullable=False),
                    sa.Column('scope', sa.String(50), nullable=False),
                    sa.Column('attachment_count', sa.Integer, nullable=False),
                    sa.Column('description', sa.Text()),
                    sa.Column('is_attachable', sa.Boolean),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('account_id',), ['account.id']),
                    sa.UniqueConstraint('arn', 'account_id'),
                    sa.Column('job_uuid', sa.String(255), nullable=False),
                    sa.Column('update_date', sa.DateTime(), nullable=False),
                    sa.Column('create_date', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False)
                    )
def downgrade():
    op.drop_table('policy')
