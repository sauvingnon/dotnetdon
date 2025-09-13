# services/3x-ui/client.py

import httpx
from config import X_UI_PANEL_SERVICE_URL

client = httpx.AsyncClient(base_url=X_UI_PANEL_SERVICE_URL)