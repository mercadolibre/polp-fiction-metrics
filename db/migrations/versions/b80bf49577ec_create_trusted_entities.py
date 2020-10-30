"""empty message
Revision ID: b80bf49577ec
Revises: 7bf0ccd79e43
Create Date: 2020-08-13 20:01:10.505811
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b80bf49577ec'
down_revision = '7bf0ccd79e43'
branch_labels = None
depends_on = None
def upgrade():    
    op.create_table('trusted_role_user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('user_id',), ['user.id']),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('role_id',), ['role.id'])
            )
    op.create_table('trusted_role_role',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.Column('assuming_role_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('assuming_role_id',), ['role.id']),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('role_id',), ['role.id'])
            )
    op.create_table('trusted_role_service',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.Column('service_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('service_id',), ['service.id']),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('role_id',), ['role.id'])
            )
    op.create_table('trusted_role_account',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.Column('account_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('account_id',), ['account.id']),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(('role_id',), ['role.id'])
            )
def downgrade():
    op.drop_table('trusted_role_user')
    op.drop_table('trusted_role_role')
    op.drop_table('trusted_role_service')
    op.drop_table('trusted_role_account')
