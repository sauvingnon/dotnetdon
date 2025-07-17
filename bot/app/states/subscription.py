# states/subscription.py

from aiogram.fsm.state import StatesGroup, State

class SubscriptionState(StatesGroup):
    choosing_plan = State()
    confirming = State()
    check_email = State()
    get_email = State()

class ConfirmEmailState(StatesGroup):
    confirm_existing = State()
    confirm_new = State()

class Step(StatesGroup):
    # Выбор платформы
    choose_platform = State()
    # Показать пользователю меню
    show_menu = State() 
    # Выслать ссылки для выбранной платформы
    send_links_for_platform = State()
    # Успешна ли загрузка приложения
    check_dowloand = State()
    # Оплата
    payment = State()
    # Отправка ключа
    send_key = State()

    waiting_for_username = State()
    # Проверка триала
    # start_trial = State()
    # Показать тарифы подписки
    # buy_subscription = State()

# Шаги FSM
class AdminSteps(StatesGroup):
    waiting_for_username = State()