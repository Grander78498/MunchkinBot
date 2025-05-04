"""Основной файл рычагов."""

import os
import sys
from pathlib import Path


from aiogram import Dispatcher, Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

from tg_bot.states import GeneralState
from tg_bot.messages import start_message

from tg_bot.utils.enums import KeyBoards

working_dir = Path().absolute().parent
sys.path.insert(0, str(working_dir))

for name in os.listdir(working_dir):
    if working_dir.joinpath(name).is_dir():
        sys.path.insert(0, str(working_dir.joinpath(name)))

try:
    from integrations import get_exchange_rate, Currencies
except ImportError as e:
    raise ImportError("Ошибка при импорте внутренних модулей") from e


router = Router(name='general')


@router.message(F.text.lower() == KeyBoards.RETURN)
async def return_handler(message: Message, state: FSMContext):
    """Обработка возвращения."""
    current_state = await state.get_state()
    match current_state:
        case GeneralState.START:
            pass
        case GeneralState.PERSONAL_ACCOUNT:
            await start_message(message)



@router.message(GeneralState.START, F.text.lower() == KeyBoards.CREATE_ROOM)
async def create_room(message: Message, state: FSMContext):
    """Создание комнаты."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.INVITE_PLAYER)
    builder.button(text=KeyBoards.START_GAME)
    builder.button(text=KeyBoards.SETUP_CONFIG)
    builder.adjust(2)

    await state.set_state(GeneralState.CREATE_ROOM)
    await message.answer(text='Создание комнаты', reply_markup=builder.as_markup())


@router.message(GeneralState.CREATE_ROOM, F.text.lower() == KeyBoards.START_GAME)
async def start_game(message: Message, state: FSMContext):
    """Начало игры."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.button(text=KeyBoards.READY)
    builder.adjust(3)

    await state.set_state(GeneralState.START_GAME)
    await message.answer(text='START_GAME_PLACEHOLDER', reply_markup=builder.as_markup())


@router.message(F.text.lower().in_(["ход текущего игрока"]))
async def current_player_move(message: Message, dp: Dispatcher):
    """Ход игрока (текущего игрока)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.OPEN_DOOR)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(text='START_GAME_PLACEHOLDER', reply_markup=builder.as_markup())

@router.message(F.text.lower().in_(["чужой ход игрока"]))
async def churka_player_move(message: Message):
    """Ход игрока (не текущего)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(text='START_GAME_PLACEHOLDER', reply_markup=builder.as_markup())


@router.message(F.text.lower().in_(["бой текущего игрока"]))
async def player_battle(message: Message):
    """бой игрока (после открытия двери и там монстр)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.REQUEST_HELP)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(text='START_GAME_PLACEHOLDER', reply_markup=builder.as_markup())


@router.message(F.text.lower().in_(["победа игрока"]))
async def player_win(message: Message):
    """Победа игрока над монстром."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.TAKE_TREASURE) # Или распределить сокровища
    builder.adjust(1)
    await message.answer(text='START_GAME_PLACEHOLDER', reply_markup=builder.as_markup())


@router.message(F.text.lower().in_(["сосание игрока"]))
async def player_lose(message: Message):
    """Игрок сосал."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.LOSE)
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(1)
    await message.answer(text='PLAYER_SUCKING_PLACEHOLDER', reply_markup=builder.as_markup())


@router.message(F.text.lower() == KeyBoards.PERSONAL_ACCOUNT)
async def personal_account(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_STATISTIC)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.RETURN)
    builder.adjust(2)

    await state.set_state(GeneralState.PERSONAL_ACCOUNT)
    await message.answer(text=KeyBoards.PERSONAL_ACCOUNT, reply_markup=builder.as_markup())


@router.message(F.text.lower().in_(["трамп", "евро", "нефритовый стержень", "бульба", "дирхам оаэ", "сингапур"]))
async def transparent_policies_v2(message: Message):
    if message is None:
        await message.answer("Произошла ошибка при отправке курса")
        return
    match message.text.lower():
        case "трамп":
            await message.reply(
                f"Курс доллара равен {get_exchange_rate(Currencies.USD)} ₽"
            )
        case "евро":
            await message.reply(
                f"Курс евро равен {get_exchange_rate(Currencies.EUR)} ₽"
            )
        case "нефритовый стержень":
            await message.reply(
                f"Курс юаня равен {get_exchange_rate(Currencies.CNY)} ₽"
            )
        case "бульба":
            await message.reply(
                f"Курс белорусского рубля равен {get_exchange_rate(Currencies.BYN)} ₽"
            )
        case "дирхам оаэ":
            await message.reply(
                f"Курс дирхама ОАЭ равен {get_exchange_rate(Currencies.AED)} ₽"
            )
        case "сингапур":
            await message.reply(
                f"Курс сингапурского доллара равен {get_exchange_rate(Currencies.SGD)} ₽"
            )
        case _:
            await message.answer("Хы")