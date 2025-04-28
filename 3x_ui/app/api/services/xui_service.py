import uuid
from py3xui import Api, Client
import config
from httpx import HTTPError

# Настройки
url = config.URL_FOR_PANEL
username = config.PANEL_LOGIN
password = config.PANEL_PASSWORD
secret_key = config.PANEL_SECRET_KEY
url_sub = config.URL_SUBSCRIPTION
inboundId = 2

# Авторизация (пока статически на старте)
api = Api(url, username, password, secret_key, use_tls_verify=False)
# api = Api(url, username, password, use_tls_verify=False)
api.login()

async def add_new_client(tg_username: str) -> str | None:
    id = str(uuid.uuid4())
    short_id = id.replace('-', '')[:10]
    sub_id = f"dotNetDon_VPN_{short_id}"
    email = f"{short_id}{tg_username}"

    try:
        new_client = Client(
            id=id,
            email=email,
            enable=True,
            inboundId=inboundId,
            flow="xtls-rprx-vision",
            limitIp=1,
            subId=sub_id,
        )

        api.client.add(inbound_id=inboundId, clients=[new_client])

        return url_sub + new_client.sub_id

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