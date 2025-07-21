# services/payment/client.py

import httpx
from config import PAYMENT_SERVICE_URL

client = httpx.AsyncClient(base_url=PAYMENT_SERVICE_URL)
