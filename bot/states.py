from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    profile = State()
    post = State()
    input_name_channel = State()
    content = State()
    admin_comment = State()
    mailing = State()

