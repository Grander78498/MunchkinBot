from aiogram.fsm.state import State, StatesGroup


class GeneralState(StatesGroup):
    START = State()
    PERSONAL_ACCOUNT = State()
    PARENT_ACCOUNT = State()

