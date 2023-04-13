from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard1 = [[InlineKeyboardButton('📝 Личный кабинет', callback_data='work_account'),  InlineKeyboardButton('🟡 Отметиться', callback_data='work_check')], [InlineKeyboardButton('🆘 Помощь', callback_data='work_help')]]
menu = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('Назад', callback_data='back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)

phone = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton('Верно', callback_data='accept_phone'), InlineKeyboardButton('Неверно', callback_data='back_phone')]])


account_menu = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton('Имя', callback_data='work_edit_name'), InlineKeyboardButton('Номер', callback_data='work_edit_phone')],
													   [InlineKeyboardButton('Табельный', callback_data='work_edit_number'), InlineKeyboardButton('Должность', callback_data='work_edit_position')],
									[InlineKeyboardButton('Назад ↩', callback_data='back')]])