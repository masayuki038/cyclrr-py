"""create users

Revision ID: 782dd74d0a45
Revises: a01087afd86f
Create Date: 2019-04-14 13:07:33.773976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782dd74d0a45'
down_revision = 'a01087afd86f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_name', sa.String(32), nullable=True),
        sa.Column('password', sa.String(64), nullable=True),
        sa.Column('first_name', sa.String(32), nullable=True),
        sa.Column('last_name', sa.String(32), nullable=True),
        sa.Column('mail', sa.String(256), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, server_default=sa.func.now()) 
    )

    op.add_column('contents', sa.Column('user_id', sa.Integer))


def downgrade():
    op.drop_table('users')
    op.drop_column('contents', 'user_id')
