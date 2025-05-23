# pylint: skip-file
"""fix field name

Revision ID: ae56d122db5d
Revises: 4c77dd162bbb
Create Date: 2025-04-22 10:52:32.187213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "ae56d122db5d"
down_revision: Union[str, None] = "4c77dd162bbb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "item",
        "runaway_bonus",
        existing_type=sa.INTEGER(),
        type_=sa.SmallInteger(),
        existing_nullable=True,
    )
    op.drop_column("item", "runway_bonus")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "item",
        sa.Column(
            "runway_bonus", sa.SMALLINT(), autoincrement=False, nullable=True
        ),
    )
    op.alter_column(
        "item",
        "runaway_bonus",
        existing_type=sa.SmallInteger(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
