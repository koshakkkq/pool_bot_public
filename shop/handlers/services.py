import asyncio
import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from shop.photos import photos
from create import bot
from shop.stickers import stickers
import shop.keyboards.services as keyboards

async def our_services_begin(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)

	await callback.message.delete()

	await callback.message.answer_photo(photo=photos["our_services"], caption="Наши услуги:\n\n1. Сервисное обслуживание бассейнов от 1800 руб/выезд в черте города.\n2. Продажа Химии для бассейна с доставкой.\n3. Строительство бассейнов под ключ.\n4. Составление ТУ для бетонных работ и 3D моделирование Вашего бассейна.\n5. Подбор и продажа оборудования для Вашего бассейна.\n6. Реконструкция Вашего действующего бассейна.\n\nВыберите цифру, чтобы почитать по подробнее 👇🏼",
										reply_markup=keyboards.shop_services_keyboard)
	await state.reset_data()
	await callback.answer()

async def our_services_begin_msg(message : types.Message, state: FSMContext):
	await message.answer_photo(photo=photos["our_services"],
										caption="Наши услуги:\n\n1. Сервисное обслуживание бассейнов от 1800 руб/выезд в черте города.\n2. Продажа Химии для бассейна с доставкой.\n3. Строительство бассейнов под ключ.\n4. Составление ТУ для бетонных работ и 3D моделирование Вашего бассейна.\n5. Подбор и продажа оборудования для Вашего бассейна.\n6. Реконструкция Вашего действующего бассейна.\n\nВыберите цифру, чтобы почитать по подробнее 👇🏼",
										reply_markup=keyboards.shop_services_keyboard)
	await state.reset_data()

async def our_services_page_1(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:
		await callback.message.answer(text="Сервисное обслуживание бассейнов\n\nОт 1800 руб/выезд в черте города",
								  reply_markup=keyboards.shop_services1_keyboard)
	else:
		await callback.message.edit_text(text="Сервисное обслуживание бассейнов\n\nОт 1800 руб/выезд в черте города",
									  reply_markup=keyboards.shop_services1_keyboard)
	await state.update_data(order_from_page="1. Сервисное обслуживание бассейнов от 1800 руб/выезд в черте города")
	await callback.answer()

async def our_services_page_2(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:

		await callback.message.answer(text="Продажа Химии для бассейна с доставкой\n\nПерейти в наш магазин 👇🏼",
								  reply_markup=keyboards.shop_services2_keyboard)
	else:
		await callback.message.edit_text(text="Продажа Химии для бассейна с доставкой\n\nПерейти в наш магазин 👇🏼",
								  reply_markup=keyboards.shop_services2_keyboard)
	await state.update_data(order_from_page="2. Продажа Химии для бассейна с доставкой. ")
	await callback.answer()

async def our_services_page_3(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:

		await callback.message.answer(text="Строительство бассейнов под ключ\n(Бетонные, комопзитные, частные, общественные)\n\nОт 1 500 000 руб",
								  reply_markup=keyboards.shop_services3_keyboard)
	else:
		await callback.message.edit_text(text="Строительство бассейнов под ключ\n(Бетонные, комопзитные, частные, общественные)\n\nОт 1 500 000 руб",
								  reply_markup=keyboards.shop_services3_keyboard)
	await state.update_data(order_from_page="3. Строительство бассейнов под ключ. ")
	await callback.answer()

async def our_services_page_4(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:

		await callback.message.answer(text="Составление ТУ для бетонных работ и 3D моделирование Вашего бассейна\n\nСтоимость работы от 17 000 рублей",
								  reply_markup=keyboards.shop_services4_keyboard)
	else:
		await callback.message.edit_text(
			text="Составление ТУ для бетонных работ и 3D моделирование Вашего бассейна\n\nСтоимость работы от 17 000 рублей",
			reply_markup=keyboards.shop_services4_keyboard)
	await state.update_data(order_from_page="4. Составление ТУ для бетонных работ и 3D моделирование Вашего бассейна. ")
	await callback.answer()

async def our_services_page_5(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:

		await callback.message.answer(
			text="Подбор и продажа оборудования для Вашего бассейна.\n\nЗаказать от 200 000 рублей",
			reply_markup=keyboards.shop_services5_keyboard)
	else:
		await callback.message.edit_text(text="Подбор и продажа оборудования для Вашего бассейна.\n\nЗаказать от 200 000 рублей",
								  reply_markup=keyboards.shop_services5_keyboard)
	await state.update_data(order_from_page="5. Подбор и продажа оборудования для Вашего бассейна. ")
	await callback.answer()

async def our_services_page_6(callback: types.CallbackQuery, state: FSMContext):
	if len(callback.message.photo) != 0:

		await callback.message.answer(
			text="Реконструкция Вашего действующего бассейна",
			reply_markup=keyboards.shop_services5_keyboard)
	else:
		await callback.message.edit_text(
			text="Реконструкция Вашего действующего бассейна",
			reply_markup=keyboards.shop_services5_keyboard)
	await state.update_data(order_from_page="6. Реконструкция Вашего действующего бассейна.")
	await callback.answer()



def register_handlers(dp: Dispatcher):
	#dp.register_message_handler(get_photo, state='*', content_types=['photo'])
	dp.register_callback_query_handler(our_services_begin, state='*', text='shop_our_services')
	dp.register_callback_query_handler(our_services_page_1, state='*', text='shop_services_1')
	dp.register_callback_query_handler(our_services_page_2, state='*', text='shop_services_2')
	dp.register_callback_query_handler(our_services_page_3, state='*', text='shop_services_3')
	dp.register_callback_query_handler(our_services_page_4, state='*', text='shop_services_4')
	dp.register_callback_query_handler(our_services_page_5, state='*', text='shop_services_5')
	dp.register_callback_query_handler(our_services_page_6, state='*', text='shop_services_6')





