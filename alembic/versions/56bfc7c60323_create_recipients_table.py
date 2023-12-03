"""create recipients table

Revision ID: 56bfc7c60323
Revises: 
Create Date: 2023-11-28 21:48:37.370174

"""
from typing import Sequence, Union

from sqlalchemy.sql import func
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '56bfc7c60323'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'recipient',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('address', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('recipient')
