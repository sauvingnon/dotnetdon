# Класс для взаимодействия с ключами
from app.services.db import order_service, user_service, key_service
from app.services.xui import xui_service
from app.models.db.user import User
from app.models.db.order import Order
import logging

logger = logging.getLogger(__name__)

async def get_access_for_user(user: User, order: Order):
    try:
        # Запрашиваем ключ от XUI панели
        client = await xui_service.create_client(user.tg_username)
        if client is None:
            print('Клиент из панели не был получен.')
            return None

        # Привязываем ключ к пользователю в базе данных
        key_object = await key_service.create_key(key_content=client.url_sub, user_id=user.id, order_id=order.id)
        if key_object is None:
            print('Не удалось создать ключ в базе данных.')
            return None

        print(f"Ключ для пользователя {user.tg_username}:{user.tg_id} добавлен\nКлюч: {client.url_sub}")
        return client.url_sub

    except Exception as e:
        logger.exception(f"Ошибка при выдаче доступа пользователю {getattr(user, 'tg_username', 'не определён')}: {e}")
        return None

