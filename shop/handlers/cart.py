import asyncio
import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from shop.store_cart import get_product_cnt
from shop.handlers.store import categories_msg, categories_call

import shop.keyboards.cart as keyboards
import shop.store_cart as store_cart
from create import picture_base_url


class CartStates(StatesGroup):
	in_cart = State()
	changing_cart = State()
	changing_product = State()


async def show_cart(callback: types.CallbackQuery, state: FSMContext):
	await state.reset_data()
	await state.set_state(CartStates.in_cart.state)
	#await callback.message.delete()
	msg = await store_cart.get_msg_products_in_cart(user_id=callback.message.chat.id)
	if msg == '':
		msg = 'Ошибка на сервере'#todo сделать какую-то клаву?
	await callback.message.edit_text(text=f'Ваша корзина:\n\n{msg}', reply_markup=keyboards.cart_menu)
	await callback.answer()

async def show_cart_msg(message: types.Message, state: FSMContext):
	await state.reset_data()
	await state.set_state(CartStates.in_cart.state)
	msg = await store_cart.get_msg_products_in_cart(user_id=message.chat.id)
	if msg == '':
		msg = 'Ошибка на сервере'#todo сделать какую-то клаву?
	await message.answer(text=f'Ваша корзина:\n\n{msg}', reply_markup=keyboards.cart_menu)

async def edit_cart(callback: types.CallbackQuery, state: FSMContext):
	await state.reset_data()
	await state.set_state(CartStates.changing_cart.state)
	keyboard = await keyboards.get_products_in_cart(callback.message.chat.id)
	#await callback.message.delete()
	await callback.message.edit_text('Выберите товар которые хотите изменить.', reply_markup=keyboard)
	await callback.answer()

async def cart_edit_product(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(CartStates.changing_product.state)
	product_id = callback.data.split('_')[-1]
	product_cnt = await get_product_cnt(callback.message.chat.id, product_id)
	await state.update_data(product_cnt = product_cnt, product_id = product_id)
	data = await state.get_data()
	product_info = await keyboards.get_product_info(cart_product_id=data['product_id'],
													user_id=callback.message.chat.id, count=data['product_cnt'])
	#await callback.message.delete()
	#await callback.message.answer_photo(photo=InputFile(product_info['photo']), reply_markup=product_info['markup'], caption=product_info['msg'])

	url = picture_base_url + product_info['photo']
	await callback.message.edit_text(text=f'[ ]({url}) {product_info["msg"]}', parse_mode="Markdown",
									 reply_markup=product_info['markup'])

async def show_editable_product(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(CartStates.changing_product.state)
	data = await state.get_data()

	product_info = await keyboards.get_product_info(cart_product_id=data['product_id'], user_id=callback.message.chat.id, count=data['product_cnt'])
	await callback.message.edit_reply_markup(reply_markup=product_info['markup'])#
	await callback.answer()

async def inc_product_count(callback: types.CallbackQuery, state: FSMContext):
	data = await  state.get_data()
	product_cnt = data.get('product_cnt', 0)
	product_cnt += 1
	await state.update_data(product_cnt=product_cnt)
	await show_editable_product(callback, state)

async def dec_product_count(callback: types.CallbackQuery, state: FSMContext):
	data = await  state.get_data()
	product_cnt = data.get('product_cnt', 2)
	if product_cnt == 1:
		await callback.answer('Должен быть хотя бы один продукт')
		return
	product_cnt -= 1
	await state.update_data(product_cnt=product_cnt)
	await show_editable_product(callback, state)

async def delete_from_cart(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	try:
		await store_cart.delete_product(user_id=callback.message.chat.id, cart_product_id=data['product_id'])
		await edit_cart(callback, state)
	except Exception as e:
		logging.error(e)


async def update_cart(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	try:
		await store_cart.update_cart(callback.message.chat.id, data['product_id'], data['product_cnt'])
		await edit_cart(callback, state)
	except Exception as e:
		logging.error(e)


class OrderStates(StatesGroup):
	pending_communication_type = State()
	pending_phone = State()

async def begin_order(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(OrderStates.pending_communication_type.state)
	await callback.message.edit_text(text='📍Где вам удобнее общаться, в мессенджере или по телефону?', reply_markup=keyboards.comm_type)


async def get_comm_type(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(OrderStates.pending_phone.state)

	comm_type = callback.data.split('_')[-1]
	if comm_type == 'mess':
		comm_type = 'Мессенджере'
	else:
		comm_type = 'Телефоне'

	await state.update_data(communication_type=comm_type)
	await callback.message.answer('📞 Поделитесь пожалуйста вашим номером, чтобы мы могли связаться с вами.', reply_markup=keyboards.contact_request)
	await callback.answer()

async def get_comm_type_msg(message: types.Message, state: FSMContext):
	await state.set_state(OrderStates.pending_communication_type.state)

	await message.answer('Воспользуйтесь кнопками!\n📞 Поделитесь пожалуйста вашим номером, чтобы мы могли связаться с вами.',
									 reply_markup=keyboards.comm_type)

async def get_phone_info(message: types.Message):
	await message.answer('📞 Поделитесь пожалуйста вашим номером, чтобы мы могли связаться с вами.',
									 reply_markup=keyboards.contact_request)

async def get_phone(message: types.Message, state: FSMContext):
	phone = message.contact['phone_number']
	data = await state.get_data()
	try:
		res = await store_cart.order(phone, message.chat.id, data['communication_type'])
		if res == False:
			await message.answer('Ошибка')
			await asyncio.sleep(0.2)
		else:
			await message.answer('Успешно')
			await asyncio.sleep(0.1)
		await categories_msg(message, state)
		pass
	except Exception as e:
		logging.error(e)

def register_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(show_cart, state='*', text='store_cart')
	dp.register_callback_query_handler(edit_cart, state=CartStates.in_cart, text='cart_edit')
	dp.register_callback_query_handler(cart_edit_product, state = CartStates.changing_cart, text_startswith = 'cart_edit_')
	dp.register_callback_query_handler(edit_cart, state = CartStates.changing_product, text = 'cart_edit_back')
	dp.register_callback_query_handler(inc_product_count, state = CartStates.changing_product, text='cart_inc_product')
	dp.register_callback_query_handler(dec_product_count, state=CartStates.changing_product, text='cart_dec_product')
	dp.register_callback_query_handler(delete_from_cart, state=CartStates.changing_product, text='cart_delete_product')
	dp.register_callback_query_handler(update_cart, state=CartStates.changing_product, text='cart_edit_save')
	dp.register_callback_query_handler(categories_call,state=OrderStates.pending_phone,text='store_categories_msg')
	dp.register_callback_query_handler(categories_call, state=OrderStates.pending_communication_type, text='store_categories_msg')
	dp.register_callback_query_handler(categories_call, state=OrderStates.pending_communication_type,
									   text='store_categories_msg')


	dp.register_callback_query_handler(begin_order, state = CartStates.in_cart, text = 'cart_order')
	dp.register_callback_query_handler(get_comm_type, state = OrderStates.pending_communication_type, text_startswith='cart_commtype')
	dp.register_message_handler(get_comm_type_msg, state=OrderStates.pending_communication_type)
	dp.register_message_handler(get_phone, state=OrderStates.pending_phone, content_types=['contact'])
	dp.register_message_handler(get_phone_info, state = OrderStates.pending_phone)