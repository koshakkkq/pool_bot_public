from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
keyboard1 = [[InlineKeyboardButton('Назад', callback_data='shop_consultation_back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)



keyboard1 = [[InlineKeyboardButton('Мессенджер', callback_data='shop_commtype_mess'), InlineKeyboardButton('Телефон', callback_data='shop_commtype_phone')]]
comm_type = InlineKeyboardMarkup(inline_keyboard=keyboard1)


contact_request = ReplyKeyboardMarkup().add(KeyboardButton('Нажмите чтобы поделиться контактом', request_contact=True))
