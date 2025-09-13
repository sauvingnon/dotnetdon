# test_entry.py
from config import load_dotenv
from app.services import remnawave_service
import asyncio

async def main():
    result = await remnawave_service.add_new_client("1234567898", None, 3)

if __name__ == "__main__":
    asyncio.run(main())
