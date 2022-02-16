from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

message_btn = "✍️ Set message"
delay_btn = "🕔 Set delay"
groups_btn = "🗂 Manage groups"


def main_keyboard() -> ReplyKeyboardMarkup:
    # Main markup keyboard

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row(KeyboardButton(message_btn), KeyboardButton(delay_btn))
    keyboard.row(groups_btn)

    return keyboard


def inline_keyboard(groups) -> InlineKeyboardMarkup:
    # Inline keyboard with

    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_list = []

    for counter, group in enumerate(groups):
        if group[-1]:
            is_on = "✅"
        else:
            is_on = ""
        btn = InlineKeyboardButton(text=f"{is_on} {group[1]}", callback_data=f"set{counter}")
        btn_list.append(btn)

    home_btn = InlineKeyboardButton(text="🏠Home", callback_data='home')
    keyboard.add(*btn_list, home_btn)

    return keyboard
