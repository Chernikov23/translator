from aiogram import Router, Bot, F 
from aiogram.types import Message, CallbackQuery, ContentType
from gpytranslate import Translator, SyncTranslator
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from utils.states import *
from keyboards import inline, reply
import os, json, time, requests
import speech_recognition as sr
from pydub import AudioSegment
import speech_recognition as sr
from utils.db import *
import random


recognizer = sr.Recognizer()
bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="MarkDown"))
router = Router()
t = SyncTranslator()

async def get_message(key, lang_code):
    file_path = os.path.join(os.path.join(os.path.dirname(__file__), 'locales'), f"{lang_code}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key)


def get_language_name(lang_code):
    if lang_code == 'de':
        return 'немецком'
    elif lang_code == 'en':
        return 'английском'
    elif lang_code == 'ru':
        return 'русском'
    elif lang_code == 'zh':
        return 'китайском'
    return lang_code

@router.callback_query(F.data == "translate")
async def start_translate(call: CallbackQuery, state: FSMContext):
    await state.set_state(Translate.word)
    await call.message.answer("Введи слово, которое ты желаешь перевести")


@router.message(Translate.word)
async def proc_lang(msg: Message, state: FSMContext):
    await state.update_data(word=msg.text)
    await state.set_state(Translate.lang)
    await msg.answer("Выберите язык для перевода", reply_markup=reply.languages)
    
    
@router.message(Translate.lang)
async def send_translate(msg: Message, state: FSMContext):
    lng = msg.text
    if lng == 'Русский':
        lng='ru'
    elif lng == 'Немецкий':
        lng='de'
    elif lng == 'Китайский':
        lng='zh'
    elif lng == 'Английский':
        lng = 'en'
    await state.update_data(lang=lng) 
    data = await state.get_data() 
    word = data.get('word') 
    lang = data.get('lang') 
    translation = t.translate(text=word, targetlang=lang)
    translated_text = translation.text
    if lang == 'de':
        lang = 'немецком'
    elif lang == 'en':
        lang = 'английском'
    elif lang == 'ru':
        lang = 'русском'
    elif lang == 'zh':
        lang == 'китайском'
    await msg.answer(f"*{word}* на {lang}:\n`{translated_text}`", reply_markup=inline.langs)
    await state.set_state(Translate.active)
    
    
    
@router.callback_query()
async def proc_callbacks(callback: CallbackQuery, state: FSMContext):
    call_data = callback.data
    user_id = callback.from_user.id

    if call_data == "save_word":
        data = await state.get_data()
        word = data.get('word')
        lang = data.get('lang')
        translation = t.translate(text=word, targetlang=lang)
        translated_text = translation.text
        cursor_dict.execute('INSERT INTO user_dictionary (user_id, original, translation, language) VALUES (?, ?, ?, ?)',
                            (user_id, word, translated_text, lang))
        conn_dict.commit()
        await callback.message.answer("Слово сохранено в ваш личный словарь.", reply_markup=inline.main)
    elif call_data == "vocabulary":
        await callback.message.answer("Выберите язык словаря", reply_markup=inline.vocabulary_languages)
    elif call_data.startswith("vocab_"):
        selected_lang = call_data.split("vocab_")[1]
        cursor_dict.execute('SELECT original, translation FROM user_dictionary WHERE user_id=? AND language=?', (user_id, selected_lang))
        rows = cursor_dict.fetchall()
        if rows:
            vocab_list = "\n".join([f"*{orig}* -> {trans}" for orig, trans in rows])
            await callback.message.answer(f"Ваш словарь ({selected_lang}):\n{vocab_list}")
        else:
            await callback.message.answer("Ваш словарь пуст.")
    elif call_data == "quiz":
        cursor_dict.execute('SELECT original, translation, language FROM user_dictionary WHERE user_id=?', (user_id,))
        rows = cursor_dict.fetchall()
        if rows:
            random.shuffle(rows)  # Shuffle the words for random order
            await state.update_data(quiz_words=rows, quiz_index=0)
            await state.set_state(Translate.quiz)
            word, _, lang = rows[0]
            lang_name = get_language_name(lang)
            await callback.message.answer(f"Напиши перевод слова: *{word}* на {lang_name}", reply_markup=inline.stop_quiz)
        else:
            await callback.message.answer("Ваш словарь пуст.", reply_markup=inline.main)
    elif call_data == "stop_quiz":
        await callback.message.answer("Опрос завершен.", reply_markup=inline.main)
        await state.clear()
    elif call_data == "back":
        await callback.message.edit_text("Приветствую! Это бот переводчик", reply_markup=inline.main)
        await state.clear()
    elif call_data.startswith('lang_'):
        langs = call_data.split("lang_")[1]
        data = await state.get_data()
        word = data.get('word')
        translation = t.translate(text=word, targetlang=langs)
        translated_text = translation.text
        if langs == 'de':
            langs = 'немецком'
        elif langs == 'en':
            langs = 'английском'
        elif langs == 'ru':
            langs = 'русском'
        elif langs == 'zh':
            langs == 'китайском'
        await callback.message.edit_text(f"*{word}* на {langs}:\n`{translated_text}`", reply_markup=inline.langs)
        await state.set_state(Translate.active)
        
        
@router.message(Translate.active)
async def messages(msg: Message, state: FSMContext):
    await state.update_data(active=False)
    await msg.answer("Бот не может обрабатывать обычные сообщения. Используйте кнопки", reply_markup=inline.main)

@router.message(Translate.quiz)
async def quiz_response(msg: Message, state: FSMContext):
    data = await state.get_data()
    quiz_words = data.get('quiz_words')
    quiz_index = data.get('quiz_index')
    correct_translation = quiz_words[quiz_index][1]

    if msg.text.strip().lower() == correct_translation.strip().lower():
        await msg.answer("✅ Правильно!")
    else:
        await msg.answer(f"❌ Неправильно! Правильный ответ: {correct_translation}")

    quiz_index += 1
    if quiz_index < len(quiz_words):
        await state.update_data(quiz_index=quiz_index)
        next_word, _, lang = quiz_words[quiz_index]
        lang_name = get_language_name(lang)
        await msg.answer(f"Напиши перевод слова: *{next_word}* на {lang_name}", reply_markup=inline.stop_quiz)
    else:
        await msg.answer("Опрос завершен. Вы прошли все слова.", reply_markup=inline.main)
        await state.clear()



@router.message(F.voice)
async def proc_voice(message: Message, state: FSMContext):
    file_id = message.voice.file_id  
    file = await bot.get_file(file_id)  
    file_path = file.file_path  
    file_name = f"{file_id}.mp3"  
    await bot.download_file(file_path, file_name)  

    headers = {"keyId": "OmpqIWCbgHPYOzsI", "keySecret": "htW6xu5d757euayX"}  
    create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"  
    query_url = "https://api.speechflow.io/asr/file/v1/query?taskId="  
    files = {"file": open(file_name, "rb")}  

    response = requests.post(create_url, headers=headers, files=files)  
    if response.status_code == 200:  
        create_result = response.json()  
        query_url += create_result["taskId"] + "&resultType=4"  
        while True:  
            response = requests.get(query_url, headers=headers)  

            if response.status_code == 200:  
                query_result = response.json()  
                if query_result["code"] == 11000:  
                    if query_result["result"]:  
                        result = query_result["result"].replace("\n\n", " ")  
                        os.remove(file_name)  
                        await state.set_state(Translate.word)
                        await state.update_data(word=result)
                        await state.set_state(Translate.lang)
                        await state.update_data(lang='en')
                        data = await state.get_data()
                        word = data.get('word')
                        lang = data.get('lang')
                        translation = t.translate(text=word, targetlang=lang)
                        translated_text = translation.text
                        if lang == 'de':
                            lang = 'немецком'
                        elif lang == 'en':
                            lang = 'английском'
                        elif lang == 'ru':
                            lang = 'русском'
                        elif lang == 'zh':
                            lang == 'китайском'
                        await message.answer(f"*{result}* на {lang}:\n`{translated_text}`", reply_markup=inline.langs)
                        await state.set_state(Translate.active)
                    break  
                elif query_result["code"] == 11001:  
                    time.sleep(3)  
                    continue  
                else:  
                    break  
            else:  
                break
            
@router.message()
async def messages(msg: Message):
    await msg.answer("Бот не может обрабатывать обычные сообщения. Используйте кнопки", reply_markup=inline.main)