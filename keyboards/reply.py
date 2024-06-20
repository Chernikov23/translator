from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Русский"),
            KeyboardButton(text="Английский"),
            KeyboardButton(text="Испанский")
        ],
        [
            KeyboardButton(text='Китайский'),
            KeyboardButton(text='Немецкий')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

languages_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Russian"),
            KeyboardButton(text="English"),
            KeyboardButton(text="Spanish")
        ],
        [
            KeyboardButton(text='Chinese'),
            KeyboardButton(text='German')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# rmk = ReplyKeyboardRemove()