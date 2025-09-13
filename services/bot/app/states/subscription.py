# states/subscription.py

from aiogram.fsm.state import StatesGroup, State

class SubscriptionState(StatesGroup):
    choosing_plan = State()
    confirming = State()
    check_email = State()
    get_email = State()
    show_menu = State() 
    waiting_for_username = State() 

class ConfirmEmailState(StatesGroup):
    confirm_existing = State()
    confirm_new = State()