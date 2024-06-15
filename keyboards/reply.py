from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Русский"),
            KeyboardButton(text="Английский")
        ],
        [
            KeyboardButton(text='Китайский'),
            KeyboardButton(text='Немецкий')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# rmk = ReplyKeyboardRemove()