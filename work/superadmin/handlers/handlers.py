import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import work.superadmin.keyboards as keyboards
from utils.phone import phone_to_normal
from work.users import get_lvl
from work.superadmin.review_file import get_review_file, delete_review
import work.superadmin.user as user

from create import super_admin_id

class SuperAdminStates(StatesGroup):
	menu = State()
	phone_pending = State()
	phone_check = State()
	deleting_by_id = State()
class SuperAdminGetNumber(StatesGroup):
	pending = State()

async def get_contact_info(msg: types.Message, state: FSMContext):
	await state.set_state(SuperAdminGetNumber.pending.state)
	await msg.answer('Мы с вами не знакомы! Отправьте свой контакт!', reply_markup=keyboards.contact_request)

async def get_contact(msg: types.Message, state: FSMContext):
	await user.update_by_phone(msg.contact['phone_number'], msg.chat.id)
	await menu(msg, state)

async def menu_callback(callback: types.CallbackQuery, state:FSMContext, callback_data = None):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return

	await callback.message.edit_text(text='Добро пожаловать в админ панель, выберите действие', reply_markup=keyboards.menu)
	await state.reset_data()
	await state.set_state(SuperAdminStates.menu.state)
	await callback.answer(callback_data)

async def menu(msg: types.Message, state: FSMContext):
	res = await user.is_exist(msg.chat.id)
	if res == False:
		await get_contact_info(msg, state)
		return
	if await get_lvl(msg.chat.id) < 2 and msg.chat.id != super_admin_id:
		return
	await msg.answer(text='Добро пожаловать в админ панель, выберите действие', reply_markup=keyboards.menu)
	await state.set_state(SuperAdminStates.menu.state)
	await state.reset_data()


async def add_user(callback: types.CallbackQuery, state:FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl = 1)
	await phone_pending_info(callback.message, state)
	await callback.answer()


async def add_admin(callback: types.CallbackQuery, state:FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl = 2)
	await phone_pending_info(callback.message, state)
	await callback.answer()


async def delete_user(callback: types.CallbackQuery, state:FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl=-1)
	await phone_pending_info(callback.message, state)
	await callback.answer()

async def add_client(callback: types.CallbackQuery, state: FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl=3)
	await phone_pending_info(callback.message, state)
	await callback.answer()


async def add_user_to_project(callback: types.CallbackQuery, state: FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl=4)
	await phone_pending_info(callback.message, state)
	await callback.answer()

async def delete_user_by_id_info(callback: types.CallbackQuery, state: FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await state.update_data(user_lvl=-2)
	await state.set_state(SuperAdminStates.deleting_by_id.state)
	await callback.message.edit_text(text='Введите id', reply_markup=keyboards.back)
	await callback.answer()

async def delete_user_by_id(message:types.Message, state: FSMContext):
	if await get_lvl(message.chat.id) < 2 and message.chat.id != super_admin_id:
		return
	id = message.text
	res = await user.delete_by_id(id)
	if res == True:
		await menu(message, state)
	else:
		await message.answer('Ошибка на сервере')
		await menu(message, state)


async def back_to_phone_pending(callback: types.CallbackQuery, state:FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	await phone_pending_info(callback.message, state)
	await callback.answer()

async def phone_pending_info(message:types.Message, state: FSMContext):
	if await get_lvl(message.chat.id) < 2 and message.chat.id != super_admin_id:
		return
	await message.edit_text(text='Введите номер телефона, в международном формате +79991234567')
	await message.edit_reply_markup(reply_markup=keyboards.back)
	await state.set_state(SuperAdminStates.phone_pending.state)

async def phone_pending(message: types.Message, state: FSMContext):
	if await get_lvl(message.chat.id) < 2 and message.chat.id != super_admin_id:
		return
	phone = message.text
	phone = await phone_to_normal(phone)
	await state.update_data(phone = phone)
	await message.answer(text=f'Номер телефона переведён в международный формат, проверьте номер: {phone}\n\n В случае ошибки введите номер явно, в формате +79991234567(с + вначале и без скобок)',
						 reply_markup=keyboards.phone)
	await state.set_state(SuperAdminStates.phone_check.state)


async def phone_accept(callback: types.CallbackQuery, state: FSMContext):
	if await get_lvl(callback.message.chat.id) < 2 and callback.message.chat.id != super_admin_id:
		return
	data = await state.get_data()
	phone = data['phone']
	lvl = data['user_lvl']
	status = False
	if lvl == -1:
		status = await user.delete(phone)
	elif lvl == 1:
		status = await user.add(user_lvl=lvl, phone=phone)
	elif lvl == 2:
		status = await user.add(user_lvl=lvl, phone=phone)
		status = status and await user.add_user_to_project(user_lvl=lvl, phone=phone)
	elif lvl == 3:
		status = await user.add_client(phone=phone)
	elif lvl == 4:
		status = await user.add_user_to_project(user_lvl=1, phone=phone)

	if status is False:
		await menu_callback(callback, state, 'Ошибка!')
	else:
		await menu_callback(callback, state, 'Успешно!')

async def get_review_file_handler(callback: types.CallbackQuery, state: FSMContext):
	path = await get_review_file(callback.message.chat.id, callback.message.message_id)
	if path is None:
		return
	file = types.InputFile(path)
	await callback.message.answer_document(document=file)
	await delete_review(path)
	await callback.answer()
	await asyncio.sleep(1)
	await menu(callback.message, state)


def register_handlers_client(dp: Dispatcher):
	#dp.register_callback_query_handler(pay_info, state='*', text_startswith='pay')

	dp.register_message_handler(menu, state='*', commands=['admin'])
	dp.register_callback_query_handler(add_admin, state=SuperAdminStates.menu, text='super_add_admin')
	dp.register_callback_query_handler(add_user, state=SuperAdminStates.menu, text = 'super_add_user')
	dp.register_callback_query_handler(delete_user, state= SuperAdminStates.menu, text='super_delete')
	dp.register_callback_query_handler(add_client, state = SuperAdminStates.menu, text = 'super_add_client')
	dp.register_callback_query_handler(add_user_to_project, state= SuperAdminStates.menu, text = 'super_add_to_project')

	dp.register_callback_query_handler(delete_user_by_id_info, state=SuperAdminStates.menu, text='super_delete_by_id')
	dp.register_message_handler(delete_user_by_id, state=SuperAdminStates.deleting_by_id)

	dp.register_callback_query_handler(get_review_file_handler, state=SuperAdminStates.menu, text= 'super_get_file')

	dp.register_message_handler(phone_pending, state=SuperAdminStates.phone_pending)
	dp.register_callback_query_handler(phone_accept, state=SuperAdminStates.phone_check, text='accept_phone')
	dp.register_callback_query_handler(back_to_phone_pending, state= SuperAdminStates.phone_check, text='back_phone')
	dp.register_callback_query_handler(menu_callback, state = SuperAdminStates.phone_pending, text='back')
	dp.register_callback_query_handler(menu_callback, state = SuperAdminStates.deleting_by_id, text='back')
	dp.register_message_handler(get_contact, state=SuperAdminGetNumber.pending, content_types=['contact'])
