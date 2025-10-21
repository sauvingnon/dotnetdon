# 💡 Все клавиатуры и команды бота
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from config import ADMIN_ID, ADMIN_ID_2
from app.helpers.check_user import check_user

ADMIN_IDS = [ADMIN_ID, ADMIN_ID_2]

# 📌 Команды, отображаемые в меню Telegram
commands = [
    BotCommand(command="start", description="🏠 Перезапуск"),
    BotCommand(command="menu", description="🚀 Главное меню")
]

# 🟢 Стартовая клавиатура
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="show_menu")]
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

def get_main_menu(tg_id) -> InlineKeyboardMarkup:
    # Базовое меню
    keyboard = [
        [InlineKeyboardButton(text="🔌 Как подключиться?", callback_data="instruction")],
        [InlineKeyboardButton(text="📜 Политика сервиса", callback_data="service_rules")],
        [InlineKeyboardButton(text="📣 Наш ТГК", url="https://t.me/+nCjamYM_nIA3MzNi")]
    ]

    # Если пользователь не использовал пробный период, покажем ему кнопку 
    if check_user(tg_id) == False: 
        keyboard.insert(0, [InlineKeyboardButton(text="🎁 Получить доступ", callback_data="start_trial")])

    # Если пользователь админ — добавляем кнопку
    if str(tg_id) in ADMIN_IDS:
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
def after_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔌 Инструкция", callback_data="instruction")],
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

# 🔐 Кнопка для добавления ключа (ссылка)
def key_add_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить ключ", url=url)]
        ]
    )