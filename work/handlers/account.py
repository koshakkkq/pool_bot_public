from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import work.user_description as user_description
import work.keyboards.menu as keyboards
from work.handlers.menu import MenuState, get_account_msg, get_account, menu_call


class AccoutnInfo(StatesGroup):
	changing = State()


async def change_name(callback: types.CallbackQuery, state:FSMContext):
	await callback.message.edit_text('Введите новое имя', reply_markup=keyboards.back)
	await state.update_data(update_type = 'name')
	await state.set_state(AccoutnInfo.changing.state)


async def change_phone(callback: types.CallbackQuery, state:FSMContext):
	await callback.message.edit_text('Введите новый номер телефона', reply_markup=keyboards.back)
	await state.update_data(update_type='phone')
	await state.set_state(AccoutnInfo.changing.state)


async def change_number(callback: types.CallbackQuery, state:FSMContext):
	await callback.message.edit_text('Введите новый табельный',  reply_markup=keyboards.back)
	await state.update_data(update_type='number')
	await state.set_state(AccoutnInfo.changing.state)


async def change_position(callback: types.CallbackQuery, state:FSMContext):
	await callback.message.edit_text('Введите новую должность',  reply_markup=keyboards.back)
	await state.update_data(update_type='position')
	await state.set_state(AccoutnInfo.changing.state)


async def get_new_val(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await user_description.update_description(message.chat.id, data['update_type'], message.text)
	await get_account_msg(message, state)


def register_handlers_client(dp: Dispatcher):
	#dp.register_callback_query_handler(pay_info, state='*', text_startswith='pay')

	dp.register_callback_query_handler(change_name, state=MenuState.account_info, text = 'work_edit_name')
	dp.register_callback_query_handler(change_phone, state=MenuState.account_info, text='work_edit_phone')
	dp.register_callback_query_handler(change_number, state=MenuState.account_info, text='work_edit_number')
	dp.register_callback_query_handler(change_position, state=MenuState.account_info, text='work_edit_position')
	dp.register_message_handler(get_new_val, state= AccoutnInfo.changing)

	dp.register_callback_query_handler(get_account, state = AccoutnInfo.changing, text='back')
	dp.register_callback_query_handler(menu_call, state=MenuState.account_info, text='back')
