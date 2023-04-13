from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


keyboard1 = [[InlineKeyboardButton('Назад', callback_data='back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('✅ Записаться на консультацию', callback_data='shop_consultation_default')],
			[InlineKeyboardButton('🚛 Заказ химии', callback_data='store_categories'), InlineKeyboardButton('⭐️О нас', callback_data='shop_about')],
			 [InlineKeyboardButton('⚡️ Наши работы', callback_data='shop_our_works'), InlineKeyboardButton('🧾 Наши услуги', callback_data='shop_our_services')],
			 [InlineKeyboardButton('Отзывы ❤️', callback_data='shop_reviews'), InlineKeyboardButton('🆘 Помощь', callback_data='shop_consultation_default')]]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)


keyboard1 = [[InlineKeyboardButton('✅ Записаться на консультацию', callback_data='shop_consultation_default')],
			[InlineKeyboardButton('⚡️ Наши работы', callback_data='shop_our_works')],
			 [InlineKeyboardButton('Назад ↩️', callback_data='shop_main_menu')]]
about_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('Google 🌏',url='https://www.google.com/search?client=safari&rls=en&q=%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD+%D0%B1%D0%B0%D1%81%D1%81%D0%B5%D0%B9%D0%BD%D0%BE%D0%B2+%E2%84%961&ie=UTF-8&oe=UTF-8&dlnr=1&sei=oSvSY8zaKq-MrwSh47KQBg#dlnr=1&lrd=0x40e3b6e070569cc3:0xf88861184499d498,1')],
			[InlineKeyboardButton('Яндекс 🌐', url='https://yandex.ru/search/?text=%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD+%D0%B1%D0%B0%D1%81%D1%81%D0%B5%D0%B9%D0%BD%D0%BE%D0%B2+1+%D1%85%D1%83%D1%82%D0%BE%D1%80+%D0%BB%D0%B5%D0%BD%D0%B8%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD&search_source=dzen_desktop_safe&src=suggest_B&lr=118588')],
			 [InlineKeyboardButton('Назад ↩️', callback_data='shop_main_menu')]]
reviews_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1)

