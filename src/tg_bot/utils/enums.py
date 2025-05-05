from enum import Enum


class Language(str, Enum):
    """Доступные языки."""

    RU = "ru"
    EN = "en"
    SLAVIC = "slavic"
    CHINA = "china"


class KeyBoards(str, Enum):
    CHECK_STATISTIC = "🍔Просмотреть статистику🍟"
    SETUP_CONFIG = "🏳️‍🌈Изменить конфигурацию🏳️‍🌈"
    PERSONAL_ACCOUNT = "🧑‍🦽‍➡️Личный кабинет🧑‍🦽‍➡️"
    INVITE_PLAYER = "👨‍❤️‍💋‍👨Пригласить игрока👨‍❤️‍💋‍👨"
    TAKE_TREASURE = "🍺Забрать сокровища🍺"
    REQUEST_HELP = "🆘Попросить помощь🆘"
    PLAY_MONSTER = "😈Сыграть монстра😈"
    READY = "🫦Подтвердить готовность🫦"
    CREATE_ROOM = "🏢Создать комнату🏢"
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
