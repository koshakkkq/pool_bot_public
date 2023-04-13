from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
keyboard1 = [[InlineKeyboardButton('Назад', callback_data='shop_our_services')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [
			[InlineKeyboardButton('1.Бассейны 25 м', callback_data='shop_works_1')], [InlineKeyboardButton('2. Композитный бассейн', callback_data='shop_works_2')],
			[InlineKeyboardButton('3. Мозаичный бассейн ', callback_data='shop_works_3')], [InlineKeyboardButton('4. Пленочный бассейн ', callback_data='shop_works_4')],
			[InlineKeyboardButton('5. Переливной бассейн ', callback_data='shop_works_5')], [InlineKeyboardButton('6. Скиммерный бассейн', callback_data='shop_works_6')],
			[InlineKeyboardButton('7. Строительные процессы ', callback_data='shop_works_7')], [InlineKeyboardButton('8. Видео', callback_data='shop_works_8')],
			[InlineKeyboardButton('9. Техническое помещение', callback_data='shop_works_9')],
			[InlineKeyboardButton('🚛 Заказ химии', callback_data='store_categories')],
			[InlineKeyboardButton('Назад ↩️', callback_data='shop_main_menu')]]

works_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [[InlineKeyboardButton('✅ Записаться на консультацию', callback_data='shop_consultation_works')],[InlineKeyboardButton('Назад ↩', callback_data='shop_our_works')]]

define_work_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)







