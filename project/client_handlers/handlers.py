import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
import project.keyboards.client as keyboards
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
import project.mailing as mailing


class ClientStates(StatesGroup):
	in_menu = State()

async def client_menu_msg(message: types.Message, state:FSMContext):
	await state.reset_data()
	keyboard = await keyboards.get_objects_keyboard(message.chat.id)
	await message.answer('Добро пожаловать в меню проектов.\n\nДля добавления информации выберите проект.', reply_markup=keyboard)
	await state.reset_data()
	await state.set_state(ClientStates.in_menu.state)


async def client_menu_call(callback: types.CallbackQuery, state: FSMContext, call_data = ""):
	await state.reset_data()
	keyboard = await keyboards.get_objects_keyboard(callback.message.chat.id)
	await callback.message.edit_text('Добро пожаловать в меню проектов.\n\nДля добавления информации выберите проект.', reply_markup=keyboard)
	await callback.answer(call_data)

async def add_subscriber(callback: types.CallbackQuery, state: FSMContext):
	subscribe_id = callback.data.split('_')[-1]
	res = await mailing.add_subscribe(callback.message.chat.id, subscribe_id)
	call_data = 'Успешно'
	if res == False:
		call_data = 'Ошибка'
	await client_menu_call(callback, state, call_data)


async def delete_subscriber(callback: types.CallbackQuery, state: FSMContext):
	subscribe_id = callback.data.split('_')[-1]
	res = await mailing.delete_subscribe(callback.message.chat.id, subscribe_id)
	call_data = 'Успешно'
	if res == False:
		call_data = 'Ошибка'
	await client_menu_call(callback, state, call_data)


def register_handlers_client(dp: Dispatcher):
	dp.register_callback_query_handler(add_subscriber, state = ClientStates.in_menu, text_startswith='add_sub_')
	dp.register_callback_query_handler(delete_subscriber, state= ClientStates.in_menu,  text_startswith='cancel_sub_')

