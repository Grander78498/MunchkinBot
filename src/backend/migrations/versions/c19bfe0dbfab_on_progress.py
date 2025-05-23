# pylint: skip-file
"""On progress

Revision ID: c19bfe0dbfab
Revises: 6bdf256496c6
Create Date: 2025-04-22 00:08:04.285041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c19bfe0dbfab"
down_revision: Union[str, None] = "6bdf256496c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("FLAME", "WOODEN", "STICK", name="itemproperty").create(
        op.get_bind()
    )
    sa.Enum(
        "HEADGEAR",
        "ARMOR",
        "FOOTGEAR",
        "ONE_HAND",
        "TWO_HAND",
        "THREE_HAND",
        "MINUS_HAND",
        name="itemtype",
    ).create(op.get_bind())
    sa.Enum("DOOR", "TREASURE", name="cardtype").create(op.get_bind())
    op.create_table(
        "card",
        sa.Column(
            "name", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False
        ),
        sa.Column(
            "image_path",
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
        ),
        sa.Column(
            "card_type",
            postgresql.ENUM(
                "DOOR", "TREASURE", name="cardtype", create_type=False
            ),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_card")),
        sa.UniqueConstraint("description", name=op.f("uq_card_description")),
        sa.UniqueConstraint("image_path", name=op.f("uq_card_image_path")),
        sa.UniqueConstraint("name", name=op.f("uq_card_name")),
    )
    op.create_table(
        "item",
        sa.Column(
            "name", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False
        ),
        sa.Column(
            "image_path",
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
        ),
        sa.Column(
            "card_type",
            postgresql.ENUM(
                "DOOR", "TREASURE", name="cardtype", create_type=False
            ),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("bonus", sa.SmallInteger(), nullable=False),
        sa.Column("runaway_bonus", sa.Integer(), nullable=True),
        sa.Column("one_shot", sa.Boolean(), nullable=False),
        sa.Column("is_big", sa.Boolean(), nullable=False),
        sa.Column("is_hireling", sa.Boolean(), nullable=False),
        sa.Column("price", sa.SmallInteger(), nullable=True),
        sa.Column(
            "item_type",
            postgresql.ENUM(
                "HEADGEAR",
                "ARMOR",
                "FOOTGEAR",
                "ONE_HAND",
                "TWO_HAND",
                "THREE_HAND",
                "MINUS_HAND",
                name="itemtype",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column(
            "item_property",
            postgresql.ENUM(
                "FLAME",
                "WOODEN",
                "STICK",
                name="itemproperty",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("runway_bonus", sa.SmallInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["card_id"], ["card.id"], name=op.f("fk_item_card_id_card")
        ),
        sa.PrimaryKeyConstraint("card_id", name=op.f("pk_item")),
        sa.UniqueConstraint("description", name=op.f("uq_item_description")),
        sa.UniqueConstraint("image_path", name=op.f("uq_item_image_path")),
        sa.UniqueConstraint("name", name=op.f("uq_item_name")),
    )
    op.create_table(
        "combat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("difference", sa.SmallInteger(), nullable=False),
        sa.Column("munchkin_can_join", sa.Boolean(), nullable=False),
        sa.Column("monster_can_join", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_runaway", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"], ["game.id"], name=op.f("fk_combat_game_id_game")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_combat")),
    )
    op.create_table(
        "munchkincombat",
        sa.Column("munchkin_id", sa.Integer(), nullable=False),
        sa.Column("combat_id", sa.Integer(), nullable=False),
        sa.Column("modifier", sa.SmallInteger(), nullable=False),
        sa.Column("runaway_bonus", sa.SmallInteger(), nullable=False),
        sa.Column("is_helping", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["combat_id"],
            ["combat.id"],
            name=op.f("fk_munchkincombat_combat_id_combat"),
        ),
        sa.ForeignKeyConstraint(
            ["munchkin_id"],
            ["munchkin.id"],
            name=op.f("fk_munchkincombat_munchkin_id_munchkin"),
        ),
        sa.PrimaryKeyConstraint(
            "munchkin_id", "combat_id", name=op.f("pk_munchkincombat")
        ),
    )
    op.alter_column(
        "munchkin",
        "gender",
        existing_type=postgresql.ENUM("MALE", "FEMALE", name="gender"),
        nullable=False,
    )
    op.alter_column(
        "munchkin", "number", existing_type=sa.SMALLINT(), nullable=False
    )
    op.alter_column(
        "munchkin", "level", existing_type=sa.SMALLINT(), nullable=False
    )
    op.alter_column(
        "munchkin", "strength", existing_type=sa.SMALLINT(), nullable=False
    )
    op.alter_column(
        "munchkin", "luck", existing_type=sa.SMALLINT(), nullable=False
    )
    op.alter_column(
        "munchkin", "runaway_bonus", existing_type=sa.SMALLINT(), nullable=False
    )
    op.create_unique_constraint(
        op.f("uq_munchkin_user_id"), "munchkin", ["user_id", "game_id"]
    )
    op.alter_column(
        "turn",
        "turn_type",
        existing_type=postgresql.ENUM(
            "KICK_DOOR",
            "LOOK_TROUBLE",
            "LOOT_ROOM",
            "CHARITY",
            "COMBAT",
            name="turntype",
        ),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "turn",
        "turn_type",
        existing_type=postgresql.ENUM(
            "KICK_DOOR",
            "LOOK_TROUBLE",
            "LOOT_ROOM",
            "CHARITY",
            "COMBAT",
            name="turntype",
        ),
        nullable=True,
    )
    op.drop_constraint(op.f("uq_munchkin_user_id"), "munchkin", type_="unique")
    op.alter_column(
        "munchkin", "runaway_bonus", existing_type=sa.SMALLINT(), nullable=True
    )
    op.alter_column(
        "munchkin", "luck", existing_type=sa.SMALLINT(), nullable=True
    )
    op.alter_column(
        "munchkin", "strength", existing_type=sa.SMALLINT(), nullable=True
    )
    op.alter_column(
        "munchkin", "level", existing_type=sa.SMALLINT(), nullable=True
    )
    op.alter_column(
        "munchkin", "number", existing_type=sa.SMALLINT(), nullable=True
    )
    op.alter_column(
        "munchkin",
        "gender",
        existing_type=postgresql.ENUM("MALE", "FEMALE", name="gender"),
        nullable=True,
    )
    op.drop_table("munchkincombat")
    op.drop_table("combat")
    op.drop_table("item")
    op.drop_table("card")
    sa.Enum("DOOR", "TREASURE", name="cardtype").drop(op.get_bind())
    sa.Enum(
        "HEADGEAR",
        "ARMOR",
        "FOOTGEAR",
        "ONE_HAND",
        "TWO_HAND",
        "THREE_HAND",
        "MINUS_HAND",
        name="itemtype",
    ).drop(op.get_bind())
    sa.Enum("FLAME", "WOODEN", "STICK", name="itemproperty").drop(op.get_bind())
    # ### end Alembic commands ###
