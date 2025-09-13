# services/db/client.py

import httpx
from config import DB_SERVICE_URL

client = httpx.AsyncClient(base_url=DB_SERVICE_URL)
