# services/3x-ui/client.py

import httpx
from config import PANEL_SERVICE_URL

client = httpx.AsyncClient(base_url=PANEL_SERVICE_URL)