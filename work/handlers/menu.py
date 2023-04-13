from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import work.users as users
import work.user_description as user_description
from work.utils import pass_correct
import work.keyboards.menu as keyboards

from create import super_admin_id

class MenuState(StatesGroup):
	in_menu = State()
	account_info = State()
	help_info = State()


async def menu(message: types.Message, state:FSMContext):
	await message.answer('Добро пожаловать в главное меню', reply_markup=keyboards.menu)
	await state.reset_data()
	await state.set_state(MenuState.in_menu.state)

async def help_info_call(callback: types.CallbackQuery, state: FSMContext):
	await callback.message.edit_text(f'Напишите [администратору](tg://user?id={super_admin_id})', reply_markup=keyboards.back, parse_mode='MarkdownV2')
	await callback.answer()
	await state.set_state(MenuState.help_info.state)

async def menu_call(callback: types.CallbackQuery, state:FSMContext, callback_data = None):
	if callback_data is not None:
		await callback.message.answer(callback_data)
	await callback.message.edit_text('Добро пожаловать в главное меню', reply_markup=keyboards.menu)
	await callback.answer()
	await state.reset_data()
	await state.set_state(MenuState.in_menu.state)

async def get_account(callback: types.CallbackQuery, state:FSMContext):
	msg = await user_description.get_description_msg(callback.message.chat.id)
	if msg != None:
		await callback.message.edit_text(text=msg, reply_markup=keyboards.account_menu)
		await callback.answer()
		await state.set_state(MenuState.account_info.state)

async def get_account_msg(message: types.Message, state:FSMContext):
	msg = await user_description.get_description_msg(message.chat.id)
	if msg != None:
		await message.answer(text=msg, reply_markup=keyboards.account_menu)
		await state.set_state(MenuState.account_info.state)

def register_handlers_client(dp: Dispatcher):

	dp.register_callback_query_handler(get_account, state=MenuState.in_menu, text = 'work_account')
	dp.register_callback_query_handler(help_info_call, state=MenuState.in_menu, text='work_help')
	dp.register_callback_query_handler(menu_call, state=MenuState.help_info, text='back')
