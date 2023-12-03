"""create location table

Revision ID: a8ee2b918a7a
Revises: fa805950e08e
Create Date: 2023-11-28 22:05:32.090997

"""
from typing import Sequence, Union


from sqlalchemy.sql import func
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a8ee2b918a7a'
down_revision: Union[str, None] = 'fa805950e08e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'location',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('address', sa.String(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False),
    )



def downgrade() -> None:
    op.drop_table('location')
