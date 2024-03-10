from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import DB_NAME
from utils.database import Database

db = Database(DB_NAME)

kb_manage = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Updates'),
            KeyboardButton(text='ELD News')
        ],
        [
            KeyboardButton(text='Insert Updates'),
            KeyboardButton(text='Insert new info')
        ],
        [
            KeyboardButton(text='Settings'),
            KeyboardButton(text='Log out')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click here"
)

kb_setting = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Admins list'),
        ],
        [
            KeyboardButton(text='Add admin'),
            KeyboardButton(text='Back')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click here"
)
kb_change_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Edit introduce'),
            KeyboardButton(text='Edit miran info')
        ],
        [
            KeyboardButton(text='Back')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click here"
)


def make_confirm_kb():
    rows = [
        InlineKeyboardButton(text='YES', callback_data='YES'),
        InlineKeyboardButton(text='NO', callback_data='NO')
    ]
    kb_inl = InlineKeyboardMarkup(
        inline_keyboard=[rows]
    )
    return kb_inl


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Cancel')]
    ],
    resize_keyboard=True
)
cancel_and_back = ReplyKeyboardMarkup(
    keyboard=[[
            KeyboardButton(text='Back'),
            KeyboardButton(text='Cancel')
         ]],
    resize_keyboard=True
)


def admin_list_kb(all_count, count=10):
    digits = []
    for i in range(count):
        digits.append(
            InlineKeyboardButton(
                text=str(i+1), callback_data=str(i)
            )
        )

    over_digits = []
    if all_count > 5:
        for i in range(count):
            over_digits.append(
                InlineKeyboardButton(
                    text=str(i+1), callback_data=str(i)
                )
            )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                over_digits,
                [
                    InlineKeyboardButton(text='⬅', callback_data='prev'),
                    InlineKeyboardButton(text='➡', callback_data='next')
                ]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[digits]
    )


modify_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✍ Edit", callback_data='edit'),
            InlineKeyboardButton(text="❌ Delete", callback_data='delete'),
        ]
    ]
)
cancel_skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Skip')],
        [KeyboardButton(text='Cancel')],
    ],
    resize_keyboard=True
)
skip_back_cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Skip')],
        [
            KeyboardButton(text='Back'),
            KeyboardButton(text='Cancel'),
        ],
    ],
    resize_keyboard=True,
)