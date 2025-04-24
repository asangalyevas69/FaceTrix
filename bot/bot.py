import asyncio
import os

from aiogram import Bot, Dispatcher 
from dotenv import load_dotenv
from handlers import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


