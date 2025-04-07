import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from pathlib import Path
from api_client import APIClient

current_path = Path().absolute()
load_dotenv(current_path.parent.parent.joinpath('.env'), override=True)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
api_client = APIClient('http://127.0.0.1:8000')


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    result = api_client.save_user(message.from_user.id,
                                  message.from_user.username)
    await message.answer(result['msg'])


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
