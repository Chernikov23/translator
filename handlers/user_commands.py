from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import inline
from utils.db import *
import json
import google.generativeai as genai
router = Router()

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
        await msg.answer("Это бот переводчик! Чтобы переводить - нажмите на кнопку. Также вы можете переводить голосовые сообщения (работает на русском языке)", reply_markup=inline.main)
    else:
        await msg.answer("Это бот переводчик! Чтобы переводить - нажмите на кнопку. Также вы можете переводить голосовые сообщения (работает на русском языке)", reply_markup=inline.main)



@router.message(Command('amount_of_users'))
async def amountOfUsers(msg: Message):
    cursor_users.execute('SELECT COUNT(*) FROM users')
    count = cursor_users.fetchone()[0]
    await msg.answer(f"Количество пользователей: *{count}*")