from enum import Enum


class Language(str, Enum):
    """Доступные языки."""

    RU = "ru"
    EN = "en"
    SLAVIC = "slavic"
    CHINA = "china"


class KeyBoards(str, Enum):
    CHECK_STATISTIC = "🍔Просмотреть статистику🍟"
    SETUP_CONFIG = "🏳️‍🌈Изменить конфигурацию пола🏳️‍🌈"
    PERSONAL_ACCOUNT = "🧑‍🦽‍➡️Личный кабинет🧑‍🦽‍➡️"
    TAKE_TREASURE = "🍺Забрать сокровища🍺"
    REQUEST_HELP = "🆘Попросить помощь🆘"
    PLAY_MONSTER = "😈Сыграть монстра😈"
    READY = "🫦Подтвердить готовность🫦"
    CREATE_ROOM = "🏢Создать комнату🏢"
    DELETE_PARTY = "💀Завершить партию💀"
    LEAVE_PARTY = "🍻Выйти из игры🍻"
    MEMBERS = "👥Участники👥"
    BAN_MEMBER = "🤬Забанить🤬"
    MEMBER_INFO = "🥸Посмотреть подробную информацию🥸"
    ACTIVE_ROOM = "➡️Перейти к текущей игре➡️"
    CHECK_CARDS = "🤲Посмотреть руку🤲"
    SETUP_CARDS = "🃏Настроить карты🃏"
    SETUP_DICE = "🎲Настроить кубик🎲"
    GET_CARD = "🫥Взять в закрытую🫥"
    JOIN_GAME = "👨‍❤️‍💋‍👨Присоединиться👨‍❤️‍💋‍👨"
    WIN_STATISTIC = "🥇Выигранные🥇"
    OPEN_DOOR = "🚪Открыть дверь🚪"
    END_TURN = "💸Завершить ход💸"
    START_GAME = "▶️Начать игру▶️"
    INVENTORY = "🎒Инвентарь🎒"
    SUPPORT = "🤝Поддержка🤝"
    RETURN = "🔙Вернуться🔙"
    DONATE = "💰Донат💰"
    LOSE = "😮Сосать😮"
