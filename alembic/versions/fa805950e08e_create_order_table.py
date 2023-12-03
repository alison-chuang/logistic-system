"""create order table

Revision ID: fa805950e08e
Revises: 56bfc7c60323
Create Date: 2023-11-28 22:03:35.326836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'fa805950e08e'
down_revision: Union[str, None] = '56bfc7c60323'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'order',
        sa.Column('sno', sa.Integer(), primary_key=True),
        sa.Column('recipient_id', sa.Integer(), sa.ForeignKey('recipient.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=func.now(), onupdate=func.now(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('order')
