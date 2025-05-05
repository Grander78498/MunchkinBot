from aiogram.fsm.state import State, StatesGroup


class GeneralState(StatesGroup):
    START = State()
    PERSONAL_ACCOUNT = State()
    CREATE_ROOM = State()
    START_GAME = State()
    JOIN_GAME = State()
    MY_TURN = State()
    OTHER_TURN = State()
