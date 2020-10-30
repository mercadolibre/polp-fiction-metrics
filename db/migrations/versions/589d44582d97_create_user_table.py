"""empty message
Revision ID: 589d44582d97
Revises: 8a631af89c52
Create Date: 2020-07-20 14:12:56.392466
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '589d44582d97'
down_revision = '8a631af89c52'
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('name', sa.String(255)),
                    sa.Column('arn', sa.String(255), nullable=False),
                    sa.Column('foreign', sa.Boolean(), nullable=False),
                    sa.Column('last_auth', sa.DateTime()),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('inline_count', sa.Integer()),
                    sa.ForeignKeyConstraint(('account_id',), ['account.id']),
                    sa.UniqueConstraint('arn', 'account_id'),
                    sa.Column('create_date', sa.DateTime()),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('job_uuid', sa.String(255), nullable=False),

                    )
#     Antes de crear la tabla pivote, que va a contener claves foraneas de las tablas POLICY y ROLES,  tenémos que crear la tabla POLICIES (la de roles la creamos arriba)
#     op.create_table('policy',
#                     sa.Column()
#                     )

def downgrade():
    op.drop_table('user')
