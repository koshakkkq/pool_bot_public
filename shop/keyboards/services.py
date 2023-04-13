from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
keyboard1 = [[InlineKeyboardButton('Назад', callback_data='shop_our_services')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [
			[InlineKeyboardButton('1', callback_data='shop_services_1'), InlineKeyboardButton('2', callback_data='shop_services_2'), InlineKeyboardButton('3', callback_data='shop_services_3')],
			[InlineKeyboardButton('4', callback_data='shop_services_4'), InlineKeyboardButton('5', callback_data='shop_services_5'), InlineKeyboardButton('6', callback_data='shop_services_6')],
			 [InlineKeyboardButton('Назад ↩️', callback_data='shop_main_menu')]]
shop_services_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [
	[InlineKeyboardButton('1/6', callback_data='empty_call'), InlineKeyboardButton('➡', callback_data='shop_services_2')],
			 [InlineKeyboardButton('Заказать ✅', callback_data='shop_consultation_services')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]
]
shop_services1_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [[InlineKeyboardButton('⬅', callback_data='shop_services_1'), InlineKeyboardButton('2/6', callback_data='empty_call'), InlineKeyboardButton('➡', callback_data='shop_services_3')],
			 [InlineKeyboardButton('🚛 Заказ химии', callback_data='store_categories')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]]
shop_services2_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)



keyboard1 = [[InlineKeyboardButton('⬅', callback_data='shop_services_2'), InlineKeyboardButton('3/6', callback_data='empty_call'), InlineKeyboardButton('➡', callback_data='shop_services_4')],
			 [InlineKeyboardButton('Заказать консультацию ✅', callback_data='shop_consultation_services')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]]
shop_services3_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('⬅', callback_data='shop_services_3'), InlineKeyboardButton('4/6', callback_data='empty_call'), InlineKeyboardButton('➡', callback_data='shop_services_5')],
			 [InlineKeyboardButton('Заказать ✅', callback_data='shop_consultation_services')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]]
shop_services4_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('⬅', callback_data='shop_services_4'), InlineKeyboardButton('5/6', callback_data='empty_call'), InlineKeyboardButton('➡', callback_data='shop_services_6')],
			 [InlineKeyboardButton('Заказать ✅', callback_data='shop_consultation_services')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]]
shop_services5_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('⬅', callback_data='shop_services_6'), InlineKeyboardButton('6/6', callback_data='empty_call')],
			 [InlineKeyboardButton('Заказать консультацию ✅', callback_data='shop_consultation_services')],
			 [InlineKeyboardButton('Назад ↩', callback_data='shop_our_services')]]
shop_services6_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)