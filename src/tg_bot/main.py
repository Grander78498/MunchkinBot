"""
Главный файл для запуска бота
"""

import asyncio
import logging
import os
import sys
import json
from enum import Enum
from pathlib import Path


current_path = Path().absolute()
sys.path.insert(0, current_path.parent.joinpath('integrations'))
sys.path.insert(0, current_path.parent.parent)

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import CallbackQuery, Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from dotenv import load_dotenv
from tg_bot.utils.api_client import APIClient
from custom_exceptions import EnvException, TGException
from integrations.exchange_rates import get_exchange_rate, Currencies


class Language(str, Enum):
    RU = 'ru'
    EN = 'en'
    SLAVIC = 'slavic'
    CHINA = 'china'


def read_text(key: str, lang: Language) -> str:
    """Считывание текстовой информации из json
    
    Args:
        key (str) - ключ
        lang (str) - язык пользователя
    """
    with open('docs.json', 'r', encoding='utf-8') as file:
        texts = json.load(file)
        return texts[key][lang]
    
load_dotenv(current_path.parent.parent.joinpath('.env'), override=True)

logging.basicConfig(level=logging.INFO)
token = os.getenv('BOT_TOKEN')
if token is None:
    raise EnvException('Отсутствует переменная среды BOT_TOKEN')

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
api_client = APIClient('http://127.0.0.1:8000')


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обработка команды start"""
    user = message.from_user
    if user is None:
        raise TGException('Ошибка при получении отправителя сообщения')
    api_client.save_user(user.id, user.username, user.full_name)
    await message.answer(read_text("start", Language.RU))


@dp.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """Обработка команды help"""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("help", Language.RU))


@dp.message(Command("rules"))
async def cmd_rules(message: types.Message) -> None:
    """Обработка команды rules"""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    builder = InlineKeyboardBuilder()
    builder.button(text='Оригинальные правила', url='https://hobbygames.ru/download/rules/m_color_rules.pdf')
    await message.answer(read_text("rules", Language.RU), reply_markup=builder.as_markup())


@dp.message(Command("support"))
async def cmd_support(message: types.Message) -> None:
    """Обработка команды support"""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("support", Language.RU))


@dp.message(Command("donate"))
async def cmd_donate(message: types.Message) -> None:
    """Обработка команды donate"""
    # Вставить получение информации о пользователе, чтобы вытягивать язык пользователя
    await message.answer(read_text("donate", Language.RU))



@dp.callback_query(F.data.in_(['tru','Ursula','XI','Bel', 'OAE', 'SGD']))
async def transparent_policies(call: CallbackQuery):
    match call.data:
        case 'tru':
            await call.message.reply(f"Тарифы!!!! {get_exchange_rate(Currencies.USD)} ₽")
        case 'Ursula':
            await call.message.reply(f"Геи негры пидарасы!!!! {get_exchange_rate(Currencies.EUR)} ₽")
        case 'XI':
            await call.message.reply(f"Тайвань - Китай!!!! {get_exchange_rate(Currencies.CNY)} ₽")
        case 'Bel':
            await call.message.reply(f"Бульба!!!! {get_exchange_rate(Currencies.BYN)} ₽")
        case 'OAE':
            await call.message.reply(f"Деньги, тачки, админки!!!! {get_exchange_rate(Currencies.AED)} ₽")
        case 'SGD':
             await call.message.reply(f"Кораблики!!!! {get_exchange_rate(Currencies.SGD)} ₽")
    await call.answer("Хы")

@dp.message(Command("get_most_transparent_policies"))
async def cmd_world(message: types.Message) -> None:
    """Выдача актуальных валют"""
    builder = InlineKeyboardBuilder()
    builder.button(text='Трамп', callback_data="tru")
    builder.button(text='Евро', callback_data="Ursula")
    builder.button(text='Нефритовый стержень', callback_data="XI")
    builder.button(text='Бульба', callback_data="Bel")
    builder.button(text='Дирхам ОАЭ', callback_data="OAE")
    builder.button(text='Сингапур', callback_data="SGD")
    builder.adjust(2)
    await message.answer("Выбери СВОего героя", reply_markup=builder.as_markup())

@dp.message(Command("get_daniel_trumps_most_transparent_policies"))
async def cmd_get_exchange_rate(message: types.Message) -> None:
    # TODO document why this method is empty
    value = get_exchange_rate(Currencies.USD)
    await message.reply(f"Актуальная политика Данилы Трампова: {value} ₽") 

@dp.message(Command("motivation"))
async def bird_with_eggs(message: types.Message) -> None:
    await message.answer_photo(caption="Яйца с птицей", photo="https://cs15.pikabu.ru/post_img/2024/12/29/4/1735451132180917891.jpg")


async def main() -> None:
    """Запуск бота"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
