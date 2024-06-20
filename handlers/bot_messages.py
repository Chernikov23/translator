from aiogram import Router, Bot, F 
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile
from gpytranslate import Translator, SyncTranslator
from config_reader import config
from aiogram.fsm.context import FSMContext
from utils.states import *
from keyboards import inline, reply
import os, json, time, requests
import speech_recognition as sr
import speech_recognition as sr
from utils.db import *
import random
from gtts import gTTS


recognizer = sr.Recognizer()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='MarkDown')
router = Router()
t = SyncTranslator()

async def get_message(key, lang_code):
    file_path = os.path.join(os.path.join(os.path.dirname(__file__), 'locales'), f"{lang_code}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key)


def get_language_name(lang_code, code):
    if lang_code == 'de':
        return 'немецком' if code =='ru' else "german"
    elif lang_code == 'en':
        return 'английском' if code == 'ru' else "english"
    elif lang_code == 'ru':
        return 'русском' if code == 'ru' else "russian"
    elif lang_code == 'zh':
        return 'китайском' if code =='ru' else "chinese"
    elif lang_code == 'es':
        return 'испанском' if code == 'ru' else "spanish"
    return lang_code

@router.callback_query(F.data == "translate")
async def start_translate(call: CallbackQuery, state: FSMContext):
    await state.set_state(Translate.word)
    await call.message.answer(text= await get_message("putWord", call.from_user.language_code))


@router.message(Translate.word)
async def proc_lang(msg: Message, state: FSMContext):
    await state.update_data(word=msg.text)
    await state.set_state(Translate.lang)
    await msg.answer(text= await get_message("chLang", msg.from_user.language_code), reply_markup=reply.languages if msg.from_user.language_code == 'ru' else reply.languages_en) 
    
    
@router.message(Translate.lang)
async def send_translate(msg: Message, state: FSMContext):
    lng = msg.text
    if lng == 'Русский' or lng == 'Russian':
        lng='ru'
    elif lng == 'Немецкий' or lng == "German":
        lng='de'
    elif lng == 'Китайский' or lng == "Chinese":
        lng='zh'
    elif lng == 'Английский' or lng == "English":
        lng = 'en'
    elif lng == 'Испанский' or lng == 'Spanish':
        lng = 'es'
    await state.update_data(lang=lng) 
    data = await state.get_data() 
    word = data.get('word') 
    lang = data.get('lang') 
    translation = t.translate(text=word, targetlang=lang)
    translated_text = translation.text
    if lang == 'de':
        lang = 'немецком' if msg.from_user.language_code == 'ru' else "german"
    elif lang == 'en':
        lang = 'английском' if msg.from_user.language_code == 'ru' else "english"
    elif lang == 'ru':
        lang = 'русском' if msg.from_user.language_code == 'ru' else "russian"
    elif lang == 'zh':
        lang == 'китайском' if msg.from_user.language_code == 'ru' else "chinese"
    elif lang == 'es':
        lang == 'испанском' if msg.from_user.language_code == 'ru' else 'spanish'
    tts = gTTS(translated_text, lang=lng)
    tts.save('translated_audio.mp3')
    await bot.send_audio(chat_id=msg.chat.id, audio=FSInputFile("translated_audio.mp3"), caption=str(await get_message("res", msg.from_user.language_code)).format(word, lang, translated_text), reply_markup=inline.langs if msg.from_user.language_code == 'ru' else inline.langs_en)
    await state.set_state(Translate.word)
    os.remove("translated_audio.mp3")
    
    
    
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
        await callback.message.answer(text=await get_message("wSaved", callback.from_user.language_code), reply_markup=inline.main if callback.from_user.language_code == 'ru' else inline.main_en)
    elif call_data == "vocabulary":
        await callback.message.answer(text=await get_message("vLang", callback.from_user.language_code), reply_markup=inline.vocabulary_languages if callback.from_user.language_code == 'ru' else inline.vocabulary_languages_en)
    elif call_data.startswith("vocab_"):
        selected_lang = call_data.split("vocab_")[1]
        cursor_dict.execute('SELECT original, translation FROM user_dictionary WHERE user_id=? AND language=?', (user_id, selected_lang))
        rows = cursor_dict.fetchall()
        if rows:
            vocab_list = "\n".join([f"*{orig}* -> {trans}" for orig, trans in rows])
            await callback.message.answer(text=str(await get_message("yVoc", callback.from_user.language_code)).format(selected_lang, vocab_list))
        else:
            await callback.message.answer(text= await get_message("vocEmp", callback.from_user.language_code))
    elif call_data == "quiz":
        cursor_dict.execute('SELECT original, translation, language FROM user_dictionary WHERE user_id=?', (user_id,))
        rows = cursor_dict.fetchall()
        if rows:
            random.shuffle(rows)  # Shuffle the words for random order
            await state.update_data(quiz_words=rows, quiz_index=0)
            await state.set_state(Translate.quiz)
            word, _, lang = rows[0]
            lang_name = get_language_name(lang, callback.from_user.language_code)
            await callback.message.answer(text=str(await get_message("stQui", callback.from_user.language_code)).format(word, lang_name), reply_markup=inline.stop_quiz if callback.from_user.language_code == 'ru' else inline.stop_quiz_en)
        else:
            await callback.message.answer(text= await get_message("vocEmp", callback.from_user.language_code), reply_markup=inline.main if callback.from_user.language_code == 'ru' else inline.main_en)
    elif call_data == "stop_quiz":
        await callback.message.answer(text=await get_message("oFin", callback.from_user.language_code), reply_markup=inline.main if callback.from_user.language_code == 'ru' else inline.main_en)
        await state.clear()
    elif call_data == "back":
        await callback.message.edit_text(text=await get_message("start", callback.from_user.language_code), reply_markup=inline.main if callback.from_user.language_code == 'ru' else inline.main_en)
        await state.clear()
    elif call_data.startswith('lang_'):
        await callback.message.delete()
        langs = call_data.split("lang_")[1]
        data = await state.get_data()
        word = data.get('word')
        lang_text = ''
        translation = t.translate(text=word, targetlang=langs)
        translated_text = translation.text
        if langs == 'de':
            lang_text = 'немецком' if callback.from_user.language_code == "ru" else 'german'
        elif langs == 'en':
            lang_text = 'английском' if callback.from_user.language_code == 'ru' else 'english'
        elif langs == 'ru':
            lang_text = 'русском' if callback.from_user.language_code == 'ru' else "russian"
        elif langs == 'zh':
            lang_text == 'китайском' if callback.from_user.language_code == 'ru' else "chinese"
        elif langs == 'es':
            lang_text == 'испанском' if callback.from_user.language_code == 'ru' else "spanish"
        tts = gTTS(translated_text, lang=langs)
        tts.save('translated_audio.mp3')
        

        await bot.send_audio(chat_id=callback.message.chat.id, audio=FSInputFile('translated_audio.mp3'), caption=str(await get_message("res", callback.from_user.language_code)).format(word, lang_text, translated_text), reply_markup=inline.langs if callback.from_user.language_code == 'ru' else inline.langs_en)
        os.remove('translated_audio.mp3')
        await state.set_state(Translate.word)
        
        
@router.message(Translate.quiz)
async def quiz_response(msg: Message, state: FSMContext):
    data = await state.get_data()
    quiz_words = data.get('quiz_words')
    quiz_index = data.get('quiz_index')
    correct_translation = quiz_words[quiz_index][1]

    if msg.text.strip().lower() == correct_translation.strip().lower():
        await msg.answer(text=await get_message("right", msg.from_user.language_code))
    else:
        await msg.answer(text=str(await get_message("noRi", msg.from_user.language_code)).format(correct_translation))

    quiz_index += 1
    if quiz_index < len(quiz_words):
        await state.update_data(quiz_index=quiz_index)
        next_word, _, lang = quiz_words[quiz_index]
        lang_name = get_language_name(lang, msg.from_user.language_code)
        await msg.answer(text=str(await get_message("stQui", msg.from_user.language_code)).format(next_word, lang_name), reply_markup=inline.stop_quiz if msg.from_user.language_code == 'ru' else inline.stop_quiz_en)
    else:
        await msg.answer(text=await get_message("oFinWord", msg.from_user.language_code), reply_markup=inline.main if msg.from_user.language_code == 'ru' else inline.main_en)
        await state.clear()



# @router.message(F.voice)
# async def proc_voice(message: Message, state: FSMContext):
#     file_id = message.voice.file_id  
#     file = await bot.get_file(file_id)  
#     file_path = file.file_path  
#     file_name = f"{file_id}.mp3"  
#     await bot.download_file(file_path, file_name)  

#     headers = {"keyId": "OmpqIWCbgHPYOzsI", "keySecret": "htW6xu5d757euayX"}  
#     create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"  
#     query_url = "https://api.speechflow.io/asr/file/v1/query?taskId="  
#     files = {"file": open(file_name, "rb")}  

#     response = requests.post(create_url, headers=headers, files=files)  
#     if response.status_code == 200:  
#         create_result = response.json()  
#         query_url += create_result["taskId"] + "&resultType=4"  
#         while True:  
#             response = requests.get(query_url, headers=headers)  

#             if response.status_code == 200:  
#                 query_result = response.json()  
#                 if query_result["code"] == 11000:  
#                     if query_result["result"]:  
#                         result = query_result["result"].replace("\n\n", " ")  
#                         os.remove(file_name)  
#                         await state.set_state(Translate.word)
#                         await state.update_data(word=result)
#                         await state.set_state(Translate.lang)
#                         await state.update_data(lang='en')
#                         data = await state.get_data()
#                         word = data.get('word')
#                         lang = data.get('lang')
#                         translation = t.translate(text=word, targetlang=lang)
#                         translated_text = translation.text
#                         if lang == 'de':
#                             lang = 'немецком'
#                         elif lang == 'en':
#                             lang = 'английском'
#                         elif lang == 'ru':
#                             lang = 'русском'
#                         elif lang == 'zh':
#                             lang == 'китайском'
#                         await message.answer(f"*{result}* на {lang}:\n`{translated_text}`", reply_markup=inline.langs)
#                         await state.set_state(Translate.active)
#                     break  
#                 elif query_result["code"] == 11001:  
#                     time.sleep(3)  
#                     continue  
#                 else:  
#                     break  
#             else:  
#                 break
@router.message(Translate.active)
async def messages(msg: Message, state: FSMContext):
    await state.update_data(active=False)
    await msg.answer(text= await get_message("noCan", msg.from_user.language_code), reply_markup=inline.main)


        
@router.message()
async def messages(msg: Message, state: FSMContext):
    await state.set_state(Translate.word)
    await state.update_data(word=msg.text)
    await state.set_state(Translate.lang)
    await msg.answer(text= await get_message("chLang", msg.from_user.language_code), reply_markup=reply.languages if msg.from_user.language_code == 'ru' else reply.languages_en)