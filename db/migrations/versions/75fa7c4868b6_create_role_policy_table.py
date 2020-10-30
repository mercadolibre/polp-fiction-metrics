"""empty message
Revision ID: 75fa7c4868b6
Revises: 18c3b62838e8
Create Date: 2020-07-20 16:00:13.642560
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '75fa7c4868b6'
down_revision = '18c3b62838e8'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('role_policy',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('role_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('role_id',), ['role.id']),
                    sa.Column('policy_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('policy_id',), ['policy.id'], ondelete="CASCADE")
                    )
def downgrade():
    op.drop_table('role_policy')
