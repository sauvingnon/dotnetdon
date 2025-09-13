import uuid
from py3xui import Api, Client
import config
from httpx import HTTPError
from app.models.client import Client as PClient
import datetime
import calendar

# Настройки
url = config.URL_FOR_PANEL
username = config.PANEL_LOGIN
password = config.PANEL_PASSWORD
secret_key = config.PANEL_SECRET_KEY
url_sub_prefix = config.URL_SUBSCRIPTION
inboundId = 1

# Авторизация (пока статически на старте)
api = Api(host=url, username=username, password=password, use_tls_verify=False)
# api = Api(url, username, password, use_tls_verify=False)
api.login()

# Обновление времени доступа для клиента - если у него вышло время, добавим месяц к текущей дате,
# если не вышло, то к дате окончанию добавим месяц
async def update_client(client_email: str, new_duration: int = None) -> bool:

    try:
        client = api.client.get_by_email(client_email)

        # Если время клиента уже вышло, то прибавим новый период к текущей дате
        if client.expiry_time < int(datetime.now(datetime.timezone.utc)):
            new_time = await get_expiry_timestamp(new_duration)
        # Если не вышло, то прибавим новый период к его дате завершения
        else:
            new_time = await add_months_to_timestamp(new_duration, client.expiry_time)

        client.expiry_time = new_time
        api.client.update(client.id, client)

        return True
    except Exception as e:
        print(f"[update_client] Ошибка при обновлении пользователя {client.email}: {e}")
        return False

async def get_client_by_email(email: str) -> Client:
    try:
        client = api.client.get_by_email(email)

        return client
    except Exception as e:
        print(f"[update_client] Ошибка при обновлении пользователя {client.email}: {e}")
        return False


async def add_new_client(tg_username: str, duration: int = None, trial_duration: int = None) -> PClient | None:
    id = str(uuid.uuid4())
    short_id = id.replace('-', '')[:10]
    sub_id = f"dotNetDon_VPN_{short_id}"
    email = f"{short_id}_{tg_username}"

    try:
        new_client = Client(
            id=id,
            email=email,
            enable=True,
            inboundId=inboundId,
            flow="xtls-rprx-vision",
            limitIp=0,
            subId=sub_id,
        )

        if duration:
            timestamp = await get_expiry_timestamp(duration)
            new_client.expiry_time = timestamp
        elif trial_duration:
            timestamp = await get_timestamp_plus_days(trial_duration)
            new_client.expiry_time = timestamp

        api.client.add(inbound_id=inboundId, clients=[new_client])

        url_sub = url_sub_prefix + new_client.sub_id

        new_p_client = PClient(
            id=id,
            email=email,
            enable=True,
            inboundId=inboundId,
            flow="xtls-rprx-vision",
            limitIp=1,
            subId=sub_id,
            url_sub=url_sub
        )

        if duration:
            new_p_client.expiryTime = timestamp
        elif trial_duration:
            new_p_client.expiryTime = timestamp

        return new_p_client

    except HTTPError as http_err:
        print(f"[add_new_client] HTTP ошибка при создании пользователя {tg_username}: {http_err}")
    except Exception as e:
        print(f"[add_new_client] Ошибка при создании пользователя {tg_username}: {e}")

    return None

async def get_clients_online():
    try:
        clients = api.client.online()
        return [str(client) for client in clients]
    except Exception as e:
        print(f"[get_clients_online] Ошибка при получении онлайн клиентов: {e}")
        return []    
    
# ✅ Генерим дату истечения через N месяцев (в миллисекундах)
async def get_expiry_timestamp(months: int = 1) -> int:
    days = months * 30  # если нет задачи быть суперточным — оставляем 30
    now = datetime.datetime.now(datetime.timezone.utc)
    expiry_date = now + datetime.timedelta(days=days)
    return int(expiry_date.timestamp() * 1000)  # переводим в миллисекунды

# ✅ Прибавляем N месяцев к дате в миллисекундах
async def add_months_to_timestamp(months: int, timestamp_ms: int) -> int:
    # Переводим миллисекунды в секунды
    timestamp = timestamp_ms / 1000
    dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    # Добавляем месяцы
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])

    new_date = datetime.datetime(year, month, day, dt.hour, dt.minute, dt.second, tzinfo=datetime.timezone.utc)

    return int(new_date.timestamp() * 1000)  # возвращаем в миллисекундах

async def get_timestamp_plus_days(count_days: int) -> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    future = now + datetime.timedelta(days=count_days)
    return int(future.timestamp() * 1000)  # миллисекунды