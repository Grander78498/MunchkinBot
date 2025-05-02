"""Кастомные исключения."""


class EnvException(Exception):
    """Исключение на случай отсутствия env файла."""


class TGException(Exception):
    """Исключение на непредвиденную ситуацию от телеграма."""
