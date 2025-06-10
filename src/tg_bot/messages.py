"""Конструкторы общих и часто используемых сообщений."""

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_marked_list, Text, Code, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.states import GeneralState
from tg_bot.utils.api_client import APIClient
from tg_bot.utils.enums import Language, KeyBoards
from tg_bot.utils.utils import read_text

from custom_exceptions.bot import TGException
from custom_exceptions.general import WrongNoneParameterException


async def start_message(
    state: FSMContext,
    message: Message | None = None,
    text: str | None = None,
    bot: Bot | None = None,
    user_id: int | None = None,
) -> None:
    """Отправка приветственного сообщения."""
    if message is not None:
        if message.from_user is None:
            raise TGException("Пользователь не пользователь")
        user_id = message.from_user.id
    elif user_id is None:
        raise WrongNoneParameterException()

    async with APIClient() as api_client:
        active_game = (await api_client.get_active_user_game(user_id)).result

    builder = ReplyKeyboardBuilder()
    if not active_game:
        builder.button(text=KeyBoards.CREATE_ROOM)
        builder.button(text=KeyBoards.JOIN_GAME)
    else:
        builder.button(text=KeyBoards.ACTIVE_ROOM)
        await state.update_data(game_code=active_game["code"], creator_id=active_game["creator_id"])
    builder.button(text=KeyBoards.SUPPORT)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.PERSONAL_ACCOUNT)
    builder.adjust(2)
    if text is None:
        text = read_text("start", Language.RU)

    await state.set_state(GeneralState.START)
    if message is not None:
        await message.answer(text=text, reply_markup=builder.as_markup())
    elif bot is not None:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=builder.as_markup())
    else:
        raise WrongNoneParameterException()


async def room_message(message: Message, state: FSMContext, text: Text | None = None) -> None:
    """Отправка сообщения с текущей игровой сессией."""
    user = message.from_user
    if user is None:
        raise TGException("Пользователь не пользователь")
    async with APIClient() as api_client:
        response = await api_client.get_active_user_game(user.id)
    active_game = response.result

    builder = ReplyKeyboardBuilder()
    if user.id == active_game["creator_id"]:
        builder.button(text=KeyBoards.START_GAME)
        builder.button(text=KeyBoards.SETUP_CONFIG)
        builder.button(text=KeyBoards.DELETE_GAME)
    else:
        builder.button(text=KeyBoards.LEAVE_GAME)

    builder.button(text=KeyBoards.MEMBERS)
    builder.button(text=KeyBoards.RETURN)
    builder.adjust(2)

    if text is None:
        text = as_list(
            Text("Код приглашения: ", Code(active_game["code"])),
            Text("Чтобы другие манчкины могли присоединиться к партии, пришлите им этот код!"),
        )

    await state.update_data(game_code=active_game["code"])
    await message.answer(**text.as_kwargs(), reply_markup=builder.as_markup())


async def members_message(message: Message, state: FSMContext) -> None:
    """Отправка сообщения с пользователями."""
    data = await state.get_data()
    async with APIClient() as api_client:
        result_list = (await api_client.get_munchkins(data["game_code"])).result_list
    text = as_marked_list(
        *[
            Text(Bold(user["full_name"]), " (", Code(user["user_name"]), ")")
            for user in result_list
        ],
        marker="👤",
    )
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.MEMBER_INFO)
    builder.button(text=KeyBoards.RETURN)

    await state.update_data(previous_state=GeneralState.ACTIVE_ROOM)
    await state.set_state(GeneralState.MEMBERS)
    await message.answer(**text.as_kwargs(), reply_markup=builder.as_markup())
