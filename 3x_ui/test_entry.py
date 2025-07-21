# test_entry.py
from config import load_dotenv
from app.services import xui_service
import asyncio

async def main():
    result = await xui_service.get_client_by_email("f184156607_adcdefg")

if __name__ == "__main__":
    asyncio.run(main())
