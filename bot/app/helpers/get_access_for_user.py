# Класс для взаимодействия с ключами
from app.services.db import order_service, user_service, key_service
from app.services.xui import xui_service

async def get_access_for_user(user_id: int, order_id: int):
    try:
        # Проверяем, существует ли заказ
        order = await order_service.get_order(order_id)
        if order is None:
            print(f"Заказ с ID {order_id} не найден.")
            return None
        
        # Проверяем, существует ли пользователь
        user = await user_service.get_user_for_user_id(user_id)
        if user is None:
            print(f"Пользователь с ID {user_id} не найден.")
            return None

        # Запрашиваем ключ от XUI панели
        key = await xui_service.add_new_client(user.tg_username)
        if not key:
            print('Ключ из панели не был получен.')
            return None

        # Привязываем ключ к пользователю в базе данных
        key_object = await key_service.create_key(key_content=key, user_id=user.id, order_id=order_id)
        if key_object is None:
            print('Не удалось создать ключ в базе данных.')
            return None

        print(f"Ключ для пользователя {user.tg_username}:{user.tg_id} добавлен\nКлюч: {key}")
        return key

    except Exception as e:
        print(f"Ошибка при выдаче доступа пользователю {user.tg_username}: {e}")
        return None
