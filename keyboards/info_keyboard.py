from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Miran Team Info'),
            KeyboardButton(text='Contact')
        ],
        [

            KeyboardButton(text='Location'),
            KeyboardButton(text='Login')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click here"
)