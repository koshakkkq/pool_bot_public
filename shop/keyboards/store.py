from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from shop.currency import get_price_in_rub
import shop.store as store



contact_request = ReplyKeyboardMarkup().add(KeyboardButton('Нажмите чтобы поделиться контактом', request_contact=True))


async def get_categories():
	res = await store.get_categories()
	buttons = []
	for i in res:
		buttons.append([InlineKeyboardButton(text=i['name'], callback_data=f'store_category_{i["id"]}')])

	buttons.append([InlineKeyboardButton(text='Перейти к корзине и оформлению.', callback_data='store_cart')])
	buttons.append([InlineKeyboardButton(text='Назад', callback_data='shop_main_menu')])
	return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_groups(category_id):
	res = await store.get_groups(category_id)
	buttons = []
	for i in res:
		buttons.append([InlineKeyboardButton(text=i['name'], callback_data=f'store_group_{i["id"]}')])

	buttons.append([InlineKeyboardButton(text='Перейти к корзине и оформлению.', callback_data='store_cart')])
	buttons.append([InlineKeyboardButton(text='Назад', callback_data='store_categories')])
	return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_products(category_id, group_id):
	res = await store.get_products(category_id, group_id)
	buttons = []
	for i in res:
		buttons.append([InlineKeyboardButton(text=i['name'], callback_data=f'store_product_{i["id"]}')])

	buttons.append([InlineKeyboardButton(text='Перейти к корзине и оформлению.', callback_data='store_cart')])
	buttons.append([InlineKeyboardButton(text='Назад', callback_data='back')])
	return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_product_info(product_id, count):
	res = await store.get_product_info(product_id)
	res['price'] = await get_price_in_rub(res['currency'], res['price'])
	new_price = res['price'] * count

	buttons = [[InlineKeyboardButton(text=f"{res['price']} * {count} = {new_price}",
									 callback_data="empty")],
			   [InlineKeyboardButton(text='-', callback_data='store_dec_product'),
				InlineKeyboardButton(text='+', callback_data='store_inc_product')],
			   [InlineKeyboardButton(text='Добавить в корзину', callback_data='store_add_to_cart')],
			   [InlineKeyboardButton(text='Перейти к корзине и оформлению.', callback_data='store_cart')],
			   [InlineKeyboardButton(text='Продолжить покупки', callback_data='back')]]

	msg = f"{res['name']}\n\n{res['description']}\n\n{res['price']} руб."
	#photo = f"shop_pictures/{res['photo']}"
	photo = f"{res['photo']}"
	return {'markup': InlineKeyboardMarkup(inline_keyboard=buttons), 'msg': msg, 'photo': photo}
