"""create tracking_status table

Revision ID: 953f9e952811
Revises: a8ee2b918a7a
Create Date: 2023-11-30 23:36:52.350718

"""
from typing import Sequence, Union

from sqlalchemy.sql import func
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '953f9e952811'
down_revision: Union[str, None] = 'a8ee2b918a7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tracking_status',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_sno', sa.Integer(), sa.ForeignKey('order.sno'), nullable=False),
        sa.Column('tracking_status', sa.String(100), nullable=True),
        sa.Column('location_id', sa.Integer(), sa.ForeignKey('location.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('tracking_status')
