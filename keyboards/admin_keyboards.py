from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Updates'),
            KeyboardButton(text='ELD News')
        ],
        [
            KeyboardButton(text='Insert Updates'),
            KeyboardButton(text='Log out'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click here"
)