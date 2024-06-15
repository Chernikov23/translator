from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📖Перевод", callback_data="translate"),
            InlineKeyboardButton(text="Словарь", callback_data="vocabulary")
        ],
        [
            InlineKeyboardButton(text="Опрос", callback_data="quiz")
        ]
    ]
)

langs = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺RU", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧EN", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton(text="🇩🇪DE", callback_data="lang_de"),
            InlineKeyboardButton(text="🇨🇳ZH", callback_data="lang_zh")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="lang_back"),
            InlineKeyboardButton(text="Сохранить слово", callback_data="save_word")
        ]
    ]
)



vocabulary_languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="vocab_ru"),
            InlineKeyboardButton(text="Английский", callback_data="vocab_en")
        ],
        [
            InlineKeyboardButton(text="Немецкий", callback_data="vocab_de"),
            InlineKeyboardButton(text="Китайский", callback_data="vocab_zh")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)

stop_quiz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Остановить опрос", callback_data="stop_quiz")
        ]
    ]
)