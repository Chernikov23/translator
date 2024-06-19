from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import inline
from utils.db import *
import os, json
router = Router()


async def get_message(key, lang_code):
    file_path = os.path.join(os.path.join(os.path.dirname(__file__), 'locales'), f"{lang_code}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key)


@router.message(CommandStart())
async def start(msg: Message):
    chat_id = msg.chat.id
    username = msg.from_user.username if msg.from_user.username else "None"
    registration_date = msg.date.strftime("%Y-%m-%d %H:%M:%S")

    cursor_users.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor_users.fetchone()

    if user is None:
        cursor_users.execute('INSERT INTO users (username, chat_id, registration_date) VALUES (?, ?, ?)', 
                        (username, chat_id, registration_date))
        conn_users.commit()
        await msg.answer(text=await get_message("start", msg.from_user.language_code), reply_markup=inline.main if msg.from_user.language_code == 'ru' else inline.main_en)
    else:
        await msg.answer(text=await get_message("start", msg.from_user.language_code), reply_markup=inline.main if msg.from_user.language_code == 'ru' else inline.main_en)



@router.message(Command('amount_of_users'))
async def amountOfUsers(msg: Message):
    cursor_users.execute('SELECT COUNT(*) FROM users')
    count = cursor_users.fetchone()[0]
    await msg.answer(f"Количество пользователей: *{count}*")