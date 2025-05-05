"""Файл со всеми командами."""

from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from tg_bot.utils.api_client import APIClient
from tg_bot.utils.utils import read_text
from tg_bot.utils.enums import Language
from tg_bot.messages import start_message
from tg_bot.states import GeneralState
from custom_exceptions.bot import TGException
from integrations import get_exchange_rate, Currencies

api_client = APIClient()
router = Router(name="commands")


@router.message(Command("start"), F.chat.type == "private")
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Обработка команды start."""
    user = message.from_user
    if user is None:
        raise TGException("Ошибка при получении отправителя сообщения")
    _ = await api_client.save_user(user.id, user.username, user.full_name)

    await start_message(message, state)


@router.message(Command("start"), F.chat.type.in_({"supergroup", "group"}))
async def cmd_group_start(message: Message) -> None:
    """Обработка команды start в группе."""
    await message.answer("Спасибо, что добавили бота в супергруппу")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обработка команды help."""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("help", Language.RU))


@router.message(Command("rules"))
async def cmd_rules(message: Message) -> None:
    """Обработка команды rules."""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Оригинальные правила",
        url="https://hobbygames.ru/download/rules/m_color_rules.pdf",
    )
    await message.answer(
        read_text("rules", Language.RU), reply_markup=builder.as_markup()
    )


@router.message(Command("support"))
async def cmd_support(message: Message) -> None:
    """Обработка команды support."""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("support", Language.RU))


@router.message(Command("donate"))
async def cmd_donate(message: Message) -> None:
    """Обработка команды donate."""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("donate", Language.RU))


@router.message(Command("get_most_transparent_policies"))
async def cmd_world(message: Message) -> None:
    """Выдача актуальных валют."""
    kb = [
        KeyboardButton(text="Трамп"),
        KeyboardButton(text="Евро"),
        KeyboardButton(text="Нефритовый стержень"),
        KeyboardButton(text="Бульба"),
        KeyboardButton(text="Дирхам ОАЭ"),
        KeyboardButton(text="Сингапур"),
    ]
    builder = ReplyKeyboardBuilder().add(*kb)
    builder.adjust(2)
    await message.answer(
        "Выбери СВОего героя", reply_markup=builder.as_markup()
    )


@router.message(Command("get_daniel_trumps_most_transparent_policies"))
async def cmd_get_exchange_rate(message: Message) -> None:
    """Получение курса доллара."""
    value = get_exchange_rate(Currencies.USD)
    await message.reply(f"Актуальная политика Данилы Трампова: {value} ₽")


@router.message(Command("motivation"))
async def bird_with_eggs(message: Message) -> None:
    """Команда для повышения мотивации."""
    await message.answer_photo(
        caption="Яйца с птицей",
        photo="https://cs15.pikabu.ru/post_img/2024/12/29/4/1735451132180917891.jpg",
    )
