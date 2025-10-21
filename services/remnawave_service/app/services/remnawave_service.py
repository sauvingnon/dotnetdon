from logger import logger
import config
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from remnawave import RemnawaveSDK
from remnawave.models import (  # Updated import path
    UsersResponseDto, 
    UserResponseDto,
    CreateUserRequestDto,
    GetAllConfigProfilesResponseDto,
    CreateInternalSquadRequestDto
)

# Настройки
base_url = config.REMNAWAVE_BASE_URL
token = config.REMNAWAVE_TOKEN

# Авторизация
remnawave = RemnawaveSDK(base_url=base_url, token=token)

async def get_all_users() -> list[UserResponseDto]:
    try:
        response = await remnawave.users.get_all_users_v2()
        users: list[UserResponseDto] = response.users
        logger.info("Все пользователи получены успешно.")
        return users
    except Exception as e:
        logger.exception(f"Ошибка при получении всех пользователей: {e}")
        return None

async def add_new_client(tg_username: str, tg_id: int | None, description: str | None, duration: int) -> UserResponseDto | None:
    try:
        logger.debug(f"Добавляем клиента {tg_username} (duration={duration}")

        if duration is not None:
            # Добавить месяцы (используем relativedelta, потому что timedelta не умеет месяцы)
            expiry_date = _get_expiry_date(duration=duration)
        else:
            expiry_date = _get_expiry_date(duration=12)

        username = f"{tg_username}_{uuid.uuid4().hex[:8]}"

        new_user = CreateUserRequestDto(
            username=username,
            expire_at=expiry_date,
            activate_all_inbounds=True,
            active_internal_squads=["4d53a152-0240-4b66-a07e-4f63dffd7916"],
            description=description,
            telegram_id=tg_id
            )
        
        logger.debug(f"Создан DTO пользователя: {new_user}")

        user = await remnawave.users.create_user(new_user)

        logger.info(f"Клиент {tg_username} успешно создан")

        return user
    except Exception as e:
        logger.exception(f"Ошибка при создании клиента {tg_username}: {e}")
        return None

# async def get_clients_online():
    
def _get_expiry_date(duration: int) -> datetime:
    now = datetime.utcnow()

    if duration:
        # Календарная прибавка месяцев — учитывает конец месяца и т.д.
        return now + relativedelta(months=duration)
    else:
        raise ValueError("Нужно указать duration или trial_duration")