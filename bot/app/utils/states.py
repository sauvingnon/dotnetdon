from aiogram.fsm.state import State, StatesGroup

class Step(StatesGroup):
    choose_platform = State()
    send_links_for_platform = State()
    check_dowloand = State()
    payment = State()
    send_key = State()