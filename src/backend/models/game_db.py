"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from sqlmodel import Field, Relationship
from backend.models import SQLModelGame


class User(SQLModelGame, table=True):
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(primary_key=True)
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)


class Group(SQLModelGame, table=True):
    """Телеграм группа"""

    __tablename__ = 'tg_group'

    tg_id: int = Field(primary_key=True)
    name: str = Field(unique=True, max_length=32)

    games: list["Game"] = Relationship(back_populates="group")


class Game(SQLModelGame, table=True):
    """Информация об игровой партии"""

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="tg_group.id")
    on_going: bool
    current_player_number: int

    group: Group = Relationship(back_populates="games")


# class PossibleGenders(SQLModelGame, table = True):
#     pass

# class Stats(SQLModelGame, table = True):
#     pass

# class StatsType(SQLModelGame, table = True):
#     pass

# class MunchkinStats(SQLModelGame, table = True):
#     pass

# class MunchkinItem(SQLModelGame, table = True):
#     pass

# class Munchkin(SQLModelGame, table = True):
#     pass

# class MunchkinCombat(SQLModelGame, table = True):
#     pass

# class MonsterCombat(SQLModelGame, table = True):
#     pass

# class Combat(SQLModelGame, table = True):
#     pass

# class MunchkinCards(SQLModelGame, table = True):
#     pass

# class Monster(SQLModelGame, table = True):
#     pass

# class UndeadType(SQLModelGame, table = True):
#     pass
