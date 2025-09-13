# services/remnawave/client.py

import httpx
from config import REMNAWAVE_PANEL_SERVICE_URL

client = httpx.AsyncClient(base_url=REMNAWAVE_PANEL_SERVICE_URL)