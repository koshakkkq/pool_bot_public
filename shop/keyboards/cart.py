from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import shop.store_cart as cart
import shop.store as store
from shop.currency import get_price_in_rub
keyboard_arr = [[InlineKeyboardButton(text='Оформить', callback_data='cart_order')],
				[InlineKeyboardButton(text='Изменить.', callback_data='cart_edit')],
				[InlineKeyboardButton(text='Назад в магазин', callback_data='store_categories')]]
cart_menu = InlineKeyboardMarkup(inline_keyboard=keyboard_arr)


keyboard_arr = [[InlineKeyboardButton(text='Отменить.', callback_data='store_categories')],]
back = InlineKeyboardMarkup(inline_keyboard=keyboard_arr)


keyboard1 = [[InlineKeyboardButton('Мессенджер', callback_data='cart_commtype_mess'), InlineKeyboardButton('Телефон', callback_data='cart_commtype_phone')], [InlineKeyboardButton(text='Отменить.', callback_data='store_categories')]]
comm_type = InlineKeyboardMarkup(inline_keyboard=keyboard1)


contact_request = ReplyKeyboardMarkup().add(KeyboardButton('Нажмите чтобы поделиться контактом', request_contact=True))

async def get_products_in_cart(user_id):
	products = await cart.get_products_in_cart(user_id)

	buttons_arr = []

	for i in products:
		buttons_arr.append([InlineKeyboardButton(text=f"{i['name']} x {i['cnt']}", callback_data=f"cart_edit_{i['id']}" )])

	buttons_arr.append([InlineKeyboardButton(text=f"Вернуться к корзине", callback_data="store_cart" )])
	return InlineKeyboardMarkup(inline_keyboard=buttons_arr)


async def get_product_info(cart_product_id, user_id, count):
	product_id = await cart.get_product_id(user_id=user_id, cart_product_id=cart_product_id)

	res = await store.get_product_info(product_id)
	res['price'] = await get_price_in_rub(res['currency'], res['price'])
	new_price = res['price'] * count

	buttons = [[InlineKeyboardButton(text=f"{res['price']} * {count} = {new_price}",
									 callback_data="empty")],
			   [InlineKeyboardButton(text='-', callback_data='cart_dec_product'), InlineKeyboardButton(text='+', callback_data='cart_inc_product')],
			   [InlineKeyboardButton(text='Удалить.', callback_data='cart_delete_product')],
			   [InlineKeyboardButton(text='Сохранить.', callback_data='cart_edit_save')],
			   [InlineKeyboardButton(text='Отменить.', callback_data='cart_edit_back')]]

	msg = f"{res['name']}\n\n{res['description']}\n\n{res['price']} руб."
	photo = f"{res['photo']}"
	return {'markup': InlineKeyboardMarkup(inline_keyboard=buttons), 'msg': msg, 'photo': photo}