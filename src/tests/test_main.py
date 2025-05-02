# src/tests/test_main.py
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, CallbackQuery, User, Chat
from aiogram.utils.keyboard import InlineKeyboardMarkup
from ..integrations.exchange_rates import get_exchange_rate, Currencies

# относительный импорт вашего кода
from ..tg_bot.main import (
    bot,
    dp,
    cmd_start,
    cmd_help,
    cmd_rules,
    cmd_support,
    cmd_donate,
    cmd_world,
    transparent_policies,
    cmd_get_exchange_rate,
    bird_with_eggs,
    read_text,
    Language,
)


@pytest.fixture(autouse=True)
def patch_api_and_text(monkeypatch, tmp_path):
    # Мокируем API‑клиент
    monkeypatch.setattr(
        "tg_bot.main.api_client.save_user", lambda *args, **kwargs: None
    )
    # Мокируем get_exchange_rate
    monkeypatch.setattr("tg_bot.main.get_exchange_rate", lambda cur: 123.0)
    # Подменяем docs.json для read_text
    data = {
        "start": {"ru": "S_RU"},
        "help": {"ru": "H_RU"},
        "rules": {"ru": "R_RU"},
        "support": {"ru": "SUP_RU"},
        "donate": {"ru": "D_RU"},
    }
    fp = tmp_path / "docs.json"
    fp.write_text(json := __import__("json").dumps(data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    yield


def make_message(command: str, lang: Language = Language.RU):
    user = User(id=1, is_bot=False, first_name="U", username="u")
    chat = Chat(id=1, type="private")
    return Message(
        message_id=1, date=None, chat=chat, from_user=user, text=f"/{command}"
    )


def make_callback(data: str):
    user = User(id=1, is_bot=False, first_name="U", username="u")
    chat = Chat(id=1, type="private")
    msg = make_message("get_most_transparent_policies")
    cb = CallbackQuery(
        id="x", from_user=user, chat_instance="ci", message=msg, data=data
    )
    return cb


@pytest.mark.asyncio
async def test_start():
    msg = make_message("start")
    msg.answer = AsyncMock()
    await cmd_start(msg)
    msg.answer.assert_called_once_with("S_RU")


@pytest.mark.asyncio
async def test_help():
    msg = make_message("help")
    msg.answer = AsyncMock()
    await cmd_help(msg)
    msg.answer.assert_called_once_with("H_RU")


@pytest.mark.asyncio
async def test_rules():
    msg = make_message("rules")
    msg.answer = AsyncMock()
    await cmd_rules(msg)
    text, kwargs = msg.answer.call_args.args[0], msg.answer.call_args.kwargs
    assert "R_RU" in text
    assert isinstance(kwargs.get("reply_markup"), InlineKeyboardMarkup)


@pytest.mark.asyncio
async def test_support_and_donate():
    for cmd, expected in [("support", "SUP_RU"), ("donate", "D_RU")]:
        msg = make_message(cmd)
        msg.answer = AsyncMock()
        await getattr(
            __import__("tg_bot.main", fromlist=[f"cmd_{cmd}"]), f"cmd_{cmd}"
        )(msg)
        assert msg.answer.call_args.args[0] == expected


@pytest.mark.asyncio
async def test_world_keyboard():
    msg = make_message("get_most_transparent_policies")
    msg.answer = AsyncMock()
    await cmd_world(msg)
    text, kwargs = msg.answer.call_args.args[0], msg.answer.call_args.kwargs
    assert "Выбери СВОего героя" in text
    assert isinstance(kwargs.get("reply_markup"), InlineKeyboardMarkup)


@pytest.mark.parametrize("code", ["tru", "Ursula", "XI", "Bel", "OAE", "SGD"])
@pytest.mark.asyncio
async def test_transparent_policies(code):
    cb = make_callback(code)
    cb.message.reply = AsyncMock()
    cb.answer = AsyncMock()
    await transparent_policies(cb)
    # reply contains mocked rate
    assert any("123.0" in call[0] for call in cb.message.reply.call_args_list)
    cb.answer.assert_called_once()


@pytest.mark.asyncio
async def test_get_exchange_rate_cmd():
    msg = make_message("get_daniel_trumps_most_transparent_policies")
    msg.reply = AsyncMock()
    await cmd_get_exchange_rate(msg)
    assert any("123.0" in call[0] for call in msg.reply.call_args_list)


@pytest.mark.asyncio
async def test_motivation():
    msg = make_message("motivation")
    msg.answer_photo = AsyncMock()
    await bird_with_eggs(msg)
    assert msg.answer_photo.call_count == 1
    _, caption, _ = msg.answer_photo.call_args.args
    assert "Яйца с птицей" in caption
