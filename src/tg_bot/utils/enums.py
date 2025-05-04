from enum import Enum


class Language(str, Enum):
    """Доступные языки."""

    RU = "ru"
    EN = "en"
    SLAVIC = "slavic"
    CHINA = "china"