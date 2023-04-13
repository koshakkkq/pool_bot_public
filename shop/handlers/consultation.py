import asyncio
import logging

from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from shop.consultation import send_to_chanel
import shop.keyboards.consultation as keyboards
from aiogram.dispatcher.filters.state import StatesGroup, State
from shop.handlers.works import our_works_begin, our_works_begin_msg
from shop.handlers.services import our_services_begin, our_services_begin_msg
from shop.handlers.greeting import client_menu, menu_msg
from create import bot
class ConsultationSates(StatesGroup):
	question_pending = State()
	communication_type_pending = State()
	phone_pending = State()

async def consultation_begin(callback: types.CallbackQuery, state: FSMContext):
	from_page = callback.data.split('_')[2]
	await state.update_data(from_page = from_page)
	if from_page != 'default':
		await consultation_page_2(callback.message, state)
		await callback.answer()
		return

	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)
	await callback.message.delete()

	await callback.message.answer(text='📝 Напишите пожалуйста какой у вас вопрос', reply_markup=keyboards.back)
	await callback.answer()
	await state.set_state(ConsultationSates.question_pending.state)


async def consultation_begin_msg(message: types.Message, state : FSMContext):
	await state.reset_data()
	await state.update_data(from_page='default')
	await message.answer(text='📝 Напишите пожалуйста какой у вас вопрос', reply_markup=keyboards.back)
	await state.set_state(ConsultationSates.question_pending.state)

async def consultation_page_2(message: types.Message, state : FSMContext):
	await message.answer(text = '📍Где вам удобнее общаться, в мессенджере или по телефону?',reply_markup=keyboards.comm_type)
	data = await state.get_data()
	if data.get('order_from_page', None) == None:
		await state.update_data(question = message.text)
	else:
		await state.update_data(question = data['order_from_page'])
	await state.set_state(ConsultationSates.communication_type_pending.state)


async def consultation_page_2_1(message: types.Message, state : FSMContext):
	await message.answer(text = 'Пожалуйста, воспользуйтесь кнопками\n📍Где вам удобнее общаться, в мессенджере или по телефону?',reply_markup = keyboards.comm_type)
	await state.set_state(ConsultationSates.communication_type_pending.state)


async def consultation_page_3(callback: types.CallbackQuery, state: FSMContext):


	await callback.message.answer(text='📞 Поделитесь пожалуйста вашим номером, чтобы мы могли связаться с вами.',
						 reply_markup=keyboards.contact_request)
	comm_type = callback.data.split('_')[-1]
	if comm_type == 'mess':
		comm_type = 'Мессенджере'
	else:
		comm_type = 'Телефоне'
	await state.update_data(communication_type=comm_type)
	await state.set_state(ConsultationSates.phone_pending.state)
	await callback.answer()


async def get_contact_info(message: types.Message):
	await message.answer(text='📞 Поделитесь пожалуйста вашим номером, чтобы мы могли связаться с вами.',
								  reply_markup=keyboards.contact_request)

async def consultation_end(message: types.Message, state : FSMContext):
	data = await state.get_data()
	phone = message.contact['phone_number']
	try:
		await send_to_chanel(name=message.from_user.first_name, communication_type=data.get('communication_type', None),
							 question=data.get('question', None), phone=phone, username = message.from_user.username, id=message.chat.id)
		await message.answer('Успешно!')
		await asyncio.sleep(0.1)
		await route_to_menu(message, state)
	except Exception as e:
		logging.error(e)
		await message.answer('Извините произошла ошибка на сервере, попробуйте ещё раз!')
		await asyncio.sleep(0.1)
		await consultation_begin_msg(message, state)


async def consultation_back(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	from_page = data.get('from_page', 'default')
	if from_page == 'works':
		await our_works_begin(callback, state)
		return
	elif from_page == 'services':
		await our_services_begin(callback, state)
		return
	else:
		await client_menu(callback, state)
		return

async def route_to_menu(message: types.Message, state : FSMContext):
	data = await state.get_data()
	from_page = data.get('from_page', 'default')
	if from_page == 'works':
		await our_works_begin_msg(message, state)
		return
	elif from_page == 'services':
		await our_services_begin_msg(message, state)
		return
	else:
		await menu_msg(message, state)
		return

def register_handlers(dp: Dispatcher):
	#dp.register_message_handler(get_photo, state='*', content_types=['photo'])
	dp.register_message_handler(consultation_page_2, state = ConsultationSates.question_pending)
	dp.register_callback_query_handler(consultation_page_3, state=ConsultationSates.communication_type_pending, text_startswith='shop_commtype')
	dp.register_message_handler(consultation_page_2_1, state=ConsultationSates.communication_type_pending)
	dp.register_message_handler(consultation_end, state=ConsultationSates.phone_pending, content_types=['contact'])
	dp.register_message_handler(get_contact_info, state =ConsultationSates.phone_pending)
	dp.register_callback_query_handler(consultation_back, state="*", text="shop_consultation_back")
	dp.register_callback_query_handler(consultation_begin, state='*', text_startswith='shop_consultation_')


