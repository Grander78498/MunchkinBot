import json

from tg_bot.utils.enums import Language


def read_text(key: str, lang: Language) -> str:
    """Считывание текстовой информации из json.

    Args:
        key (str) - ключ
        lang (str) - язык пользователя
    """
    with open("docs.json", "r", encoding="utf-8") as file:
        texts: dict[str, dict[str, str]] = json.load(file)
        return texts[key][lang]
