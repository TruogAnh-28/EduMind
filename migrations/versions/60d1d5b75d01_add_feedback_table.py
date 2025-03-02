"""add feedback table

Revision ID: 60d1d5b75d01
Revises: 3c0b0428b10f
Create Date: 2025-01-24 21:45:09.442047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60d1d5b75d01'
down_revision: Union[str, None] = '3c0b0428b10f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommend_lessons', sa.Column('bookmark', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recommend_lessons', 'bookmark')
    # ### end Alembic commands ###
