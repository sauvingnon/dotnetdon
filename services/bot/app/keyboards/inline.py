# 💡 Все клавиатуры и команды бота
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from app.schemas.db.user import User
from config import ADMIN_ID, ADMIN_ID_2

ADMIN_IDS = [ADMIN_ID, ADMIN_ID_2]

# 📌 Команды, отображаемые в меню Telegram
commands = [
    BotCommand(command="start", description="🏠 Перезапуск"),
    BotCommand(command="menu", description="🚀 Главное меню")
    # BotCommand(command="help", description="🆘 Помощь")
    # BotCommand(command="subscribe", description="💳 Подписаться")
]

# 🟢 Стартовая клавиатура
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="show_menu")]
    ]
)

# Подтверждение Да\Нет
def email_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="no")],
    ])

input_email_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", callback_data="payment")]
    ]
)

empty_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
    ]
)

# 📱 Клавиатура выбора платформы
platform_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍏 iPhone", callback_data="platform_ios")],
        [InlineKeyboardButton(text="🤖 Android", callback_data="platform_android")]
        # [InlineKeyboardButton(text="🪟 Windows", callback_data="platform_windows")],
        # [InlineKeyboardButton(text="🍎 macOS", callback_data="platform_macos")],
        # [InlineKeyboardButton(text="📺 Smart TV", callback_data="platform_smarttv")]
    ]
)

# 📥 Клавиатура после скачивания
download_check_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я скачал!", callback_data="success_dowloand")],
        [InlineKeyboardButton(text="⚠️ Проблемы, нужны другие ссылки", callback_data="error_dowloand")]
    ]
)

# ✅ После повторной отправки ссылок
keyboard_after_all_links = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я скачал!", callback_data="success_dowloand")]
    ]
)

def get_main_menu(user: User) -> InlineKeyboardMarkup:
    # Базовое меню
    keyboard = [
        # [InlineKeyboardButton(text="💳 Купить/Продлить", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="🧾 Мои ключи", callback_data="my_subscriptions")],
        # [InlineKeyboardButton(text="⚙️ Помощь", callback_data="help")],
        [InlineKeyboardButton(text="🔌 Как подключиться?", callback_data="instruction")],
        # [InlineKeyboardButton(text="📣 О нас", callback_data="about_us")],
        # [InlineKeyboardButton(text="👨‍💻 Техподдержка", url="https://t.me/sauvingnon")],
        [InlineKeyboardButton(text="📜 Политика сервиса", callback_data="service_rules")],
        [InlineKeyboardButton(text="📣 Наш ТГК", url="https://t.me/+nCjamYM_nIA3MzNi")]
        # [InlineKeyboardButton(text="🤝 Партнерская программа", callback_data="partner_programm")]
    ]

    # Если пользователь не использовал пробный период, покажем ему кнопку 
    if user.test_used == False:
        keyboard.insert(0, [InlineKeyboardButton(text="🎁 Пробный период", callback_data="start_trial")])

    # Если пользователь админ — добавляем кнопку
    if str(user.tg_id) in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton(text="🛠 Админ-панель", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# 🛠 Админ панель
admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔌 Добавить пользователя", callback_data="add_admin_user")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
    ]
)

# Оплата и проверка оплаты
def payment_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", url=url)],
            [InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_payment")],
            [InlineKeyboardButton(text="🏠 Отмена", callback_data="show_menu")]
        ]
    )

# Оплата и проверка оплаты
def after_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔌 Инструкция", callback_data="instruction")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
        ]
    )

def extend_key_keyboard(key_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Продлить", callback_data=f"extend_{key_id}")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
        ]
    )

def soon_expire_key_message(key_sub_url: str, days_left: int):
    return (
        f"Привет друг! У тебя скоро истечет подписка на ключ ```{key_sub_url}```.\n"
        f"Осталось {days_left} дней. Не забудь продлить!"
    )

def expire_key_message(key_sub_url):
    return (
        f"Привет друг! Твой ключ ```{key_sub_url}``` уже истек.\n"
        "Доступ к сервису заблокирован. Продли подписку, чтобы снова пользоваться нашим сервисом."
    )

# 💸 Тарифы на подписку
plans_tariff = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 мес — 99₽", callback_data="plan_1m")],
        [InlineKeyboardButton(text="3 мес — 279₽", callback_data="plan_3m")],
        [InlineKeyboardButton(text="6 мес — 549₽", callback_data="plan_6m")],
        [InlineKeyboardButton(text="12 мес — 999₽", callback_data="plan_12m")],
        [InlineKeyboardButton(text="📘 Инструкция покупки ключа", callback_data="instruction_for_buy_key")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
    ]
)


# 🛠 Меню помощи
help_manu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔌 Как подключиться?", callback_data="instruction")],
        # [InlineKeyboardButton(text="🎥 Видео-инструкции", callback_data="video_help")],
        # [InlineKeyboardButton(text="✉️ Написать в техподдержку", url="https://t.me/sauvingnon")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
    ]
)

# ℹ️ Меню "О нас"
about_us_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить/Продлить", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="⭐️ Отзывы", callback_data="feedback")],
        [InlineKeyboardButton(text="📣 Наш ТГК", url="https://t.me/dotnetdon")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="show_menu")]
    ]
)



# 🔐 Кнопка для добавления ключа (ссылка)
def key_add_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить ключ", url=url)]
        ]
    )