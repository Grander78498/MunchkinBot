from aiogram.fsm.state import State, StatesGroup


class GeneralState(StatesGroup):
    START = State()
    PERSONAL_ACCOUNT = State()
    ACTIVE_ROOM = State()
    START_GAME = State()
    JOIN_GAME = State()
    MEMBERS = State()
    ENTER_MEMBER_USER_NAME = State()
    MEMBER_INFO = State()
    MY_TURN = State()
    OTHER_TURN = State()
