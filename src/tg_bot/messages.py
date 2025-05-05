from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, Text, Code

from tg_bot.utils.utils import read_text
from tg_bot.utils.enums import Language, KeyBoards
from tg_bot.utils.api_client import APIClient
from tg_bot.states import GeneralState

api_client = APIClient()


async def start_message(message: Message, state: FSMContext, text: str | None = None):
    active_game = api_client.get_active_user_game(message.from_user.id)['result']

    builder = ReplyKeyboardBuilder()
    if active_game is None:
        builder.button(text=KeyBoards.CREATE_ROOM)
        builder.button(text=KeyBoards.JOIN_GAME)
    else:
        builder.button(text=KeyBoards.ACTIVE_ROOM)
        await state.update_data(game_code=active_game['code'], creator_id=active_game['creator_id'])
    builder.button(text=KeyBoards.SUPPORT)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.PERSONAL_ACCOUNT)
    builder.adjust(2)
    if text is None:
        text = read_text('start', Language.RU)
        
    await state.set_state(GeneralState.START)
    await message.answer(text=text, reply_markup=builder.as_markup())


async def room_message(message: Message, state: FSMContext, text: Text | None = None):
    user = message.from_user
    data = await state.get_data()

    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.INVITE_PLAYER)
    if user.id == data['creator_id']:
        builder.button(text=KeyBoards.START_GAME)
        builder.button(text=KeyBoards.SETUP_CONFIG)
    builder.button(text=KeyBoards.RETURN)
    builder.adjust(2)

    if text is None:
        text = as_list(
            Text("Код приглашения: ", Code(data['game_code'])),
            Text("Чтобы другие манчкины могли присоединиться к партии, пришлите им этот код!")
        )
    
    await message.answer(**text.as_kwargs(), reply_markup=builder.as_markup())