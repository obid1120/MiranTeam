from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

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
            KeyboardButton(text='Add admin')
        ],
        [
            KeyboardButton(text='Modify admin'),
            KeyboardButton(text='Remove admin')
        ],
        [
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
            KeyboardButton(text='Modify introduce'),
            KeyboardButton(text='Modify miran info')
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

