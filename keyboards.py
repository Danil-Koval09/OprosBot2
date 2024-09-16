from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_start_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Начать регистрацию')
    markup.add(btn)
    return markup


def generate_gender_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton(text='М')
    female = KeyboardButton(text='Ж')
    markup.row(male, female)
    return markup


def generate_payment_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    card = KeyboardButton(text='card')
    crypto = KeyboardButton(text='crypto')
    markup.row(card, crypto)
    return markup
