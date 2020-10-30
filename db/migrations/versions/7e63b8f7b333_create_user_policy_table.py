"""empty message
Revision ID: 7e63b8f7b333
Revises: 75fa7c4868b6
Create Date: 2020-07-21 12:45:26.752146
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7e63b8f7b333'
down_revision = '75fa7c4868b6'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('user_policy',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('user_id',), ['user.id']),
                    sa.Column('policy_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('policy_id',), ['policy.id'], ondelete="CASCADE")
                    )
def downgrade():
    op.drop_table('user_policy')
