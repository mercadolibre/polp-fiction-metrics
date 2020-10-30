"""empty message
Revision ID: fad4c9db0f72
Revises: 7e63b8f7b333
Create Date: 2020-07-21 13:04:48.255882
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fad4c9db0f72'
down_revision = '7e63b8f7b333'
branch_labels = None
depends_on = None
def upgrade():
    service_table = op.create_table('service',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('name', sa.String(255), nullable=False),
                   sa.UniqueConstraint('name'),
                    sa.Column('holds_data', sa.Boolean(), default=False),
                    sa.Column('critical', sa.Boolean(), default=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False)
                    )

def downgrade():
    op.drop_table('service')

