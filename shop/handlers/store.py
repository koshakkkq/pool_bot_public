import asyncio
import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from create import picture_base_url, bot

import shop.keyboards.store as keyboards
import shop.store_cart as store_cart

class StoreStates(StatesGroup):
	in_category = State()
	in_group = State()
	in_products = State()
	in_product_info = State()

async def categories_handler(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)
	await callback.message.delete()
	await state.reset_data()
	await state.set_state(StoreStates.in_category.state)
	keyboard = await keyboards.get_categories()
	await callback.message.answer(text='Выберите категорию.', reply_markup=keyboard)
	await callback.answer()


async def categories_msg(message: types.message, state: FSMContext):
	await state.reset_data()
	await state.set_state(StoreStates.in_category.state)
	keyboard = await keyboards.get_categories()
	await message.answer(text='Выберите категорию.', reply_markup=keyboard)

async def categories_call(callback : types.CallbackQuery, state: FSMContext):
	await categories_msg(callback.message, state)
	await callback.answer()


async def category_pick(callback: types.CallbackQuery, state: FSMContext):
	category_id = callback.data.split('_')[-1]
	await state.update_data(category_id=category_id)
	await group_handler(callback, state)

async def group_handler(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(StoreStates.in_group.state)
	data = await state.get_data()
	keyboard = await keyboards.get_groups(data['category_id'])
	await callback.message.delete()
	await callback.message.answer(text='Выберите группу.', reply_markup=keyboard)
	await callback.answer()




async def group_pick(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(StoreStates.in_products.state)
	group_id = callback.data.split('_')[-1]
	await state.update_data(group_id=group_id)
	await products_handler(callback, state)

async def products_handler(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(StoreStates.in_products.state)
	data = await state.get_data()
	category_id = data['category_id']
	keyboard = await keyboards.get_products(category_id, data['group_id'])
	#await callback.message.delete()
	await callback.message.edit_text(text='Выберите товар.', reply_markup=keyboard)
	await callback.answer()


async def product_info(callback: types.CallbackQuery, state: FSMContext):
	await state.set_state(StoreStates.in_product_info.state)
	product_id = callback.data.split('_')[-1]
	await state.update_data(product_id=product_id)
	await state.update_data(product_cnt=1)
	product_info = await keyboards.get_product_info(product_id, 1)
	#await callback.message.delete()
	#await callback.message.answer_photo(photo=InputFile(product_info['photo']), reply_markup=product_info['markup'], caption=product_info['msg'])
	url = picture_base_url+product_info['photo']
	await callback.message.edit_text(text=f'[ ]({url}) {product_info["msg"]}',parse_mode="Markdown",reply_markup=product_info['markup'])
	#await callback.answer()


async def inc_products(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	product_cnt = data.get('product_cnt', 0)
	product_cnt += 1
	await show_product(callback, state, product_cnt)

async def dec_products(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	product_cnt = data.get('product_cnt', 2)
	if product_cnt == 1:
		await callback.answer('Должен быть хотя бы один продукт')
		return
	product_cnt -= 1
	await show_product(callback, state, product_cnt)

async def show_product(callback: types.CallbackQuery, state: FSMContext, product_cnt):
	await state.set_state(StoreStates.in_product_info.state)
	data = await state.get_data()
	await state.update_data(product_cnt=product_cnt)
	product_id = data.get('product_id', None)
	if product_id == None:
		await callback.answer('Ошибка!')
		return
	product_info = await keyboards.get_product_info(product_id, product_cnt)
	await callback.message.edit_reply_markup(reply_markup=product_info['markup'])
	await callback.answer()

async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('product_id', None) is None:
		await callback.answer('Ошибка на сервере! Товар не добавлен.')
		return
	if data.get('product_cnt', None) is None:
		await callback.answer('Ошибка на сервере! Товар не добавлен.')
		return

	res = await store_cart.add_to_cart(user_id=callback.message.chat.id, product_id=data.get('product_id'), count=data.get('product_cnt'))
	if res == False:
		await callback.answer('Ошибка на сервере! Товар не добавлен.')
		return
	else:
		await callback.answer('Товар успешно добавлен.')


def register_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(categories_handler, state='*', text='store_categories')

	dp.register_callback_query_handler(category_pick, state=StoreStates.in_category, text_startswith='store_category_')
	dp.register_callback_query_handler(group_pick, state=StoreStates.in_group, text_startswith='store_group_')
	dp.register_callback_query_handler(product_info, state=StoreStates.in_products, text_startswith='store_product_')
	dp.register_callback_query_handler(inc_products, state=StoreStates.in_product_info, text = 'store_inc_product')
	dp.register_callback_query_handler(dec_products, state=StoreStates.in_product_info, text='store_dec_product')
	dp.register_callback_query_handler(add_to_cart, state = StoreStates.in_product_info, text='store_add_to_cart')

	dp.register_callback_query_handler(group_handler, state = StoreStates.in_products, text = 'back')
	dp.register_callback_query_handler(products_handler, state=StoreStates.in_product_info, text = 'back')
