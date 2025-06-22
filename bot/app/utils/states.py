from aiogram.fsm.state import State, StatesGroup

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