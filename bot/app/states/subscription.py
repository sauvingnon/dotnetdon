# states/subscription.py

from aiogram.fsm.state import StatesGroup, State

class SubscriptionState(StatesGroup):
    choosing_plan = State()
    confirming = State()
    input_email = State()
