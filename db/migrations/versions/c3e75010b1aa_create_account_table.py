"""empty message
Revision ID: c3e75010b1aa
Revises: 
Create Date: 2020-07-16 16:11:25.226866
"""
from alembic import op
# TODO: Remove datetime import, not needed on production 
from datetime import datetime
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c3e75010b1aa'
down_revision = None
branch_labels = None
depends_on = None

# Notemos que la tabla 'role' NO tiene la columna policies... como es una relación Many to Many (ya que un Role puede muchas policies y las policies pueden estar asignada a varios (many) roles AL MISMO TIEMPO)
# para eso creamos una tabla 'pivote' role_policies que es la que mantiene esta relación.
def upgrade():
    account_table  =op.create_table('account',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.Column('uuid', sa.String(255), nullable=False),
                    sa.UniqueConstraint('uuid'),
                    sa.Column('foreign', sa.Boolean(), nullable=False),
                    sa.Column('blacklisted', sa.Boolean()),
                    sa.Column('name', sa.String(255)),
                    sa.Column('job_uuid', sa.String(255)),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False)
                    )   

def downgrade():
    op.drop_table('account')




