from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_marked_list, Text, Code, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.states import GeneralState
from tg_bot.utils.api_client import APIClient
from tg_bot.utils.enums import Language, KeyBoards
from tg_bot.utils.utils import read_text

api_client = APIClient()


async def start_message(
        message: Message, state: FSMContext, text: str | None = None
):
    active_game = (await api_client.get_active_user_game(message.from_user.id)).result

    builder = ReplyKeyboardBuilder()
    if active_game is None:
        builder.button(text=KeyBoards.CREATE_ROOM)
        builder.button(text=KeyBoards.JOIN_GAME)
    else:
        builder.button(text=KeyBoards.ACTIVE_ROOM)
        await state.update_data(
            game_code=active_game["code"], creator_id=active_game["creator_id"]
        )
    builder.button(text=KeyBoards.SUPPORT)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.PERSONAL_ACCOUNT)
    builder.adjust(2)
    if text is None:
        text = read_text("start", Language.RU)

    await state.set_state(GeneralState.START)
    await message.answer(text=text, reply_markup=builder.as_markup())


async def room_message(
        message: Message, state: FSMContext, text: Text | None = None
):
    user = message.from_user
    # TODO: заменить на апи запрос, опционально, т.к. можно "вернуться" к текущей игре, удалившись из неё
    active_game = (await api_client.get_active_user_game(message.from_user.id)).result

    builder = ReplyKeyboardBuilder()
    # builder.button(text=KeyBoards.INVITE_PLAYER)
    if user.id == active_game["creator_id"]:
        builder.button(text=KeyBoards.START_GAME)
        builder.button(text=KeyBoards.SETUP_CONFIG)
        builder.button(text=KeyBoards.DELETE_PARTY)
    else:
        builder.button(text=KeyBoards.LEAVE_PARTY)

    builder.button(text=KeyBoards.MEMBERS)
    builder.button(text=KeyBoards.RETURN)
    builder.adjust(2)

    if text is None:
        text = as_list(
            Text("Код приглашения: ", Code(active_game["code"])),
            Text(
                "Чтобы другие манчкины могли присоединиться к партии, пришлите им этот код!"
            ),
        )

    await state.update_data(game_code=active_game["code"])
    await message.answer(**text.as_kwargs(), reply_markup=builder.as_markup())


async def members_message(message: Message, state: FSMContext):
    data = await state.get_data()
    result = (await api_client.get_munchkins(data['game_code'])).result
    text = as_marked_list(
        *[Text(Bold(user['full_name']), " (", Code(user['user_name']), ")") for user in result],
        marker='👤'
    )
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.MEMBER_INFO)
    builder.button(text=KeyBoards.RETURN)

    await state.update_data(previous_state=GeneralState.ACTIVE_ROOM)
    await state.set_state(GeneralState.MEMBERS)
    await message.answer(**text.as_kwargs(), reply_markup=builder.as_markup())