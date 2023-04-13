from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

keyboard1 = [[InlineKeyboardButton('Добавить админа', callback_data='super_add_admin'),  InlineKeyboardButton('Добавить в /work', callback_data='super_add_user')],
			 [InlineKeyboardButton('Добавить в /project', callback_data='super_add_to_project'), InlineKeyboardButton('Добавить клиента', callback_data='super_add_client')],
			 [InlineKeyboardButton('Забрать доступ', callback_data='super_delete'), InlineKeyboardButton('Забрать доступ по tg id', callback_data='super_delete_by_id')],
			 [InlineKeyboardButton('Получить выгрузку за месяц', callback_data='super_get_file')]]
menu = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('Назад', callback_data='back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)

phone = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton('Верно', callback_data='accept_phone'), InlineKeyboardButton('Неверно', callback_data='back_phone')]])

contact_request = ReplyKeyboardMarkup().add(KeyboardButton('Нажмите чтобы поделиться контактом', request_contact=True))