from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def consent_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Я согласен")]],
        resize_keyboard=True
    )


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text="Начать маршрут", request_location=True)],
        [KeyboardButton(text="Завершить маршрут")]
        ],
        resize_keyboard=True
    )