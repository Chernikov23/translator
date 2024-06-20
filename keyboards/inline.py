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

main_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📖Translate", callback_data="translate"),
            InlineKeyboardButton(text="Vocabluary", callback_data="vocabulary")
        ],
        [
            InlineKeyboardButton(text="Quiz", callback_data="quiz")
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
            InlineKeyboardButton(text="🇨🇳ZH", callback_data="lang_zh"),
            InlineKeyboardButton(text="🇪🇸ES", callback_data="lang_es")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="lang_back"),
            InlineKeyboardButton(text="Сохранить слово", callback_data="save_word")
        ]
    ]
)

langs_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺RU", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧EN", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton(text="🇩🇪DE", callback_data="lang_de"),
            InlineKeyboardButton(text="🇨🇳ZH", callback_data="lang_zh"),
            InlineKeyboardButton(text="🇪🇸ES", callback_data="lang_es")
        ],
        [
            InlineKeyboardButton(text="🔙Back", callback_data="back"),
            InlineKeyboardButton(text="Save word", callback_data="save_word")
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
            InlineKeyboardButton(text="Испанский", callback_data="vocab_es"),
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ]
)


vocabulary_languages_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Russian", callback_data="vocab_ru"),
            InlineKeyboardButton(text="English", callback_data="vocab_en")
        ],
        [
            InlineKeyboardButton(text="German", callback_data="vocab_de"),
            InlineKeyboardButton(text="Chinese", callback_data="vocab_zh")
        ],
        [
            InlineKeyboardButton(text="Spanis", callback_data="vocab_es"),
            InlineKeyboardButton(text="Back", callback_data="back")
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

stop_quiz_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Stop quiz", callback_data="stop_quiz")
        ]
    ]
)

