"""migrate from rails

Revision ID: a01087afd86f
Revises: 
Create Date: 2019-04-14 12:35:05.876891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a01087afd86f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'contents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(256), nullable=True),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('enabled', sa.Boolean, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, server_default=sa.func.now()) 
    )

def downgrade():
    op.drop_table('contents')
