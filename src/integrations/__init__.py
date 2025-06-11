"""Модуль для работы с интеграциями."""

from integrations.exchange_rates import Currencies, get_exchange_rate

__all__ = (Currencies, get_exchange_rate)
