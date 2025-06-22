# Класс для взаимодействия с ключами
from app.services.db import order_service, user_service, key_service
from app.services.xui import xui_service
import logging

logger = logging.getLogger(__name__)

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
        client = await xui_service.create_client(user.tg_username)
        if client is None:
            print('Клиент из панели не был получен.')
            return None

        # Привязываем ключ к пользователю в базе данных
        key_object = await key_service.create_key(key_content=client.url_sub, user_id=user.id, order_id=order_id)
        if key_object is None:
            print('Не удалось создать ключ в базе данных.')
            return None

        print(f"Ключ для пользователя {user.tg_username}:{user.tg_id} добавлен\nКлюч: {client.url_sub}")
        return client.url_sub

    except Exception as e:
        logger.exception(f"Ошибка при выдаче доступа пользователю {getattr(user, 'tg_username', 'не определён')}: {e}")
        return None

