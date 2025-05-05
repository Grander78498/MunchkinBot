"""Основной файл рычагов."""

from aiogram import Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, Text, Code, Bold

from tg_bot.utils.api_client import APIClient
from tg_bot.states import GeneralState
from tg_bot.messages import start_message, room_message
from tg_bot.utils.enums import KeyBoards
from integrations import get_exchange_rate, Currencies

api_client = APIClient()
router = Router(name="general")


@router.message(F.text == KeyBoards.RETURN)
async def return_handler(message: Message, state: FSMContext):
    """Обработка возвращения."""
    previous_state = (await state.get_data()).get("previous_state")
    await state.set_state(previous_state)
    match previous_state:
        case GeneralState.START | None:
            await start_message(message, state)
        case GeneralState.PERSONAL_ACCOUNT:
            pass


@router.message(GeneralState.START, F.text == KeyBoards.CREATE_ROOM)
async def create_room(message: Message, state: FSMContext):
    """Создание комнаты."""

    result = await api_client.create_game(message.from_user.id)
    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.CREATE_ROOM)
    if not result["ok"]:
        builder = ReplyKeyboardBuilder()
        builder.button(text=KeyBoards.RETURN)
        await message.answer(
            text=result["detail"], reply_markup=builder.as_markup()
        )
    game = result["result"]
    text = as_list(
        Text(
            "Игровая партия создана с кодом приглашения: ", Code(game["code"])
        ),
        Text(
            "Чтобы другие манчкины могли присоединиться к партии, пришлите им этот код!"
        ),
    )
    await state.update_data(
        game_code=game["code"], creator_id=game["creator_id"]
    )
    await room_message(message, state, text=text)


@router.message(GeneralState.START, F.text == KeyBoards.ACTIVE_ROOM)
async def active_room(message: Message, state: FSMContext):
    """Заход в активную комнату."""
    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.ACTIVE_ROOM)
    await room_message(message, state)


@router.message(GeneralState.START, F.text == KeyBoards.JOIN_GAME)
async def join_game(message: Message, state: FSMContext):
    """Присоединение к игре."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.RETURN)

    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.JOIN_GAME)
    await message.answer(
        "Введите код приглашения", reply_markup=builder.as_markup()
    )


@router.message(GeneralState.JOIN_GAME, F.text)
async def entered_invite_code(message: Message, state: FSMContext):
    """Обработка ввода кода приглашения."""
    result = await api_client.add_user_to_game(
        message.text, message.from_user.id
    )
    if not result["ok"]:
        builder = ReplyKeyboardBuilder()
        builder.button(text=KeyBoards.RETURN)
        await message.answer(
            result["detail"], reply_markup=builder.as_markup()
        )
        return

    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.START)
    await start_message(
        message,
        state,
        text="Вам удалось присоединиться к игре, ожидайте её начала",
    )


@router.message(GeneralState.JOIN_GAME)
async def entered_incorrect_invite_code(message: Message):
    """Обработка ввода кода приглашения, если прислали не текст."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.RETURN)
    await message.answer(
        "Мадагаскарская птица не может быть кодом приглашения, повторите ввод",
        reply_markup=builder.as_markup(),
    )


@router.message(GeneralState.CREATE_ROOM, F.text == KeyBoards.START_GAME)
async def start_game(message: Message, state: FSMContext):
    """Начало игры."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.button(text=KeyBoards.READY)
    builder.adjust(3)

    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.START_GAME)
    await message.answer(
        text="START_GAME_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(F.text.lower().in_(["ход текущего игрока"]))
async def current_player_move(message: Message, dp: Dispatcher):
    """Ход игрока (текущего игрока)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.OPEN_DOOR)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(
        text="START_GAME_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(F.text.lower().in_(["чужой ход игрока"]))
async def churka_player_move(message: Message):
    """Ход игрока (не текущего)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(
        text="START_GAME_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(F.text.lower().in_(["бой текущего игрока"]))
async def player_battle(message: Message):
    """бой игрока (после открытия двери и там монстр)."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.REQUEST_HELP)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(2)
    await message.answer(
        text="START_GAME_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(F.text.lower().in_(["победа игрока"]))
async def player_win(message: Message):
    """Победа игрока над монстром."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.TAKE_TREASURE)  # Или распределить сокровища
    builder.adjust(1)
    await message.answer(
        text="START_GAME_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(F.text.lower().in_(["сосание игрока"]))
async def player_lose(message: Message):
    """Игрок сосал."""
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.LOSE)
    builder.button(text=KeyBoards.CHECK_CARDS)
    builder.button(text=KeyBoards.INVENTORY)
    builder.adjust(1)
    await message.answer(
        text="PLAYER_SUCKING_PLACEHOLDER", reply_markup=builder.as_markup()
    )


@router.message(StateFilter(GeneralState.ACTIVE_ROOM, GeneralState.CREATE_ROOM), F.text == KeyBoards.DELETE_PARTY)
async def delete_party(message: Message, state: FSMContext):
    data = await state.get_data()
    await api_client.delete_game(data['game_code'])
    await start_message(message, state)
    

@router.message(GeneralState.ACTIVE_ROOM, F.text == KeyBoards.LEAVE_PARTY)
async def leave_party(message: Message, state: FSMContext):
    data = await state.get_data()
    await api_client.delete_user_from_game(data['game_code'], message.from_user.id)
    await start_message(message, state)


@router.message(GeneralState.START, F.text == KeyBoards.PERSONAL_ACCOUNT)
async def personal_account(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CHECK_STATISTIC)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.RETURN)
    builder.adjust(2)

    await state.update_data(previous_state=await state.get_state())
    await state.set_state(GeneralState.PERSONAL_ACCOUNT)
    await message.answer(
        text=KeyBoards.PERSONAL_ACCOUNT, reply_markup=builder.as_markup()
    )


@router.message(
    F.text.lower().in_(
        [
            "трамп",
            "евро",
            "нефритовый стержень",
            "бульба",
            "дирхам оаэ",
            "сингапур",
        ]
    )
)
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
