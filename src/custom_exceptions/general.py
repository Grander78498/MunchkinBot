"""Исключения, связанные с настройками переменных окружения."""


class EnvException(Exception):
    """Исключение на случай отсутствия env файла."""


class CodeGenerationException(RecursionError):
    """Исключение на случай неостанавливающейся генерации кода игры."""


class WrongNoneParameterException(Exception):
    """Исключение на случай одновременно переданных None параметров."""
