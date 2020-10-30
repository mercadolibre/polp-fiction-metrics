"""empty message
Revision ID: 7bf0ccd79e43
Revises: fad4c9db0f72
Create Date: 2020-07-21 16:19:08.138407
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7bf0ccd79e43'
down_revision = 'fad4c9db0f72'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('permission',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('service_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('service_id',), ['service.id']),
                    sa.Column('policy_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('policy_id',), ['policy.id'], ondelete="CASCADE"),
                    sa.Column('reading', sa.Boolean()),
                    sa.Column('writing', sa.Boolean()),
                    sa.Column('listing', sa.Boolean()),
                    sa.Column('tagging', sa.Boolean()),
                    sa.Column('last_auth_entity', sa.String(255)),
                    sa.Column('job_uuid', sa.String(255), nullable=False),
                    sa.Column('managing', sa.Boolean()),
                    sa.Column('last_used', sa.DateTime()),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False)

                    )
def downgrade():
    op.drop_table('permission')
