import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from work.handlers.menu import MenuState, menu_call, menu
import work.check
from work.users import get_lvl
import work.keyboards.check as keyboards
from work.utils import get_cur_time
from work.user_description import is_description_full



class CheckState(StatesGroup):
	object_name_pick = State()
	get_date = State()
	get_works_type = State()
	get_reagents = State()
	get_payment = State()
	check_info = State()
	editor = State()
	editor_object = State()

class ObjectsAdd(StatesGroup):
	name_pending = State()

async def check_begin(callback: types.CallbackQuery, state: FSMContext):#todo проверка на заполненость профиля!!
	if await is_description_full(callback.message.chat.id) == False:
		await callback.message.answer('Прежде чем отметиться заполните профиль! (Вкладка личный кабинет)')
		await callback.answer()
		await asyncio.sleep(1)
		await menu(callback.message, state)
		return
	await state.update_data(page = 1)
	await objects_show(callback, state)

async def objects_show(callback: types.CallbackQuery, state: FSMContext, edit_text = False):
	data = await state.get_data()

	keyboard = await keyboards.get_objects_keyboard(data['page'], callback.message.chat.id)
	await callback.message.edit_text(text='1. Выберите пожалуйста название объекта', reply_markup=keyboard)
	await callback.answer()
	await state.set_state(CheckState.object_name_pick.state)


async def next_object(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await state.update_data(page=data['page']+1)
	await objects_show(callback, state)

async def prev_object(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await state.update_data(page=data['page'] - 1)
	await objects_show(callback, state)


async def add_object(callback: types.CallbackQuery, state: FSMContext):
	lvl = await get_lvl(callback.message.chat.id)
	if lvl < 2:
		return
	await callback.message.edit_text(text='Введите имя объекта', reply_markup=keyboards.back)
	await state.set_state(ObjectsAdd.name_pending.state)

async def objects_pick_msg(message: types.Message, state: FSMContext):
	data = await state.get_data()
	keyboard = await keyboards.get_objects_keyboard(data['page'], message.chat.id)
	await message.answer(text='1. Выберите пожалуйста название объекта', reply_markup=keyboard)
	await state.set_state(CheckState.object_name_pick.state)


async def get_object_name(message: types.Message, state: FSMContext):
	lvl = await get_lvl(message.chat.id)
	if lvl < 2:
		return
	res = await work.check.add_object(message.text)
	if res == False:
		await message.answer('Ошбика на сервере')
	else:
		await message.answer('Успешно')
	await objects_pick_msg(message, state)


async def pick_object(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	id = callback.data.split('_')[3]
	await state.update_data(object_id = id)
	await state.update_data(object = await work.check.get_object_name(id))
	keyboard = await keyboards.get_time_keyboard(callback.message.chat.id)
	if data.get('edit', False) == False:
		await callback.message.answer(text='2. Укажите сегодняшнюю дату и время', reply_markup=keyboard)
		await state.set_state(CheckState.get_date.state)
		await callback.answer()
	else:
		await callback.answer()
		await get_check_info(callback.message, state)



async def delete_object(callback: types.CallbackQuery, state: FSMContext):
	lvl = await get_lvl(callback.message.chat.id)
	if lvl < 2:
		return
	data = await state.get_data()
	object_id = data.get('object_id', None)
	if object_id is None:
		await objects_show(callback, state)
	res = await work.check.delete_object(object_id)
	await state.update_data(page=1)
	await objects_show(callback, state)

async def pick_date(callback: types.CallbackQuery, state: FSMContext):
	cur_time = await get_cur_time()
	data = await state.get_data()
	await state.update_data(date = cur_time)
	if data.get('edit', False) == False:
		await callback.message.answer(
			text='3. Напишите, какие работы были проведены *написать необходимо одним сообщением')
		await state.set_state(CheckState.get_works_type.state)
		await callback.answer()
	else:
		await callback.answer()
		await get_check_info(callback.message, state)


async def pick_date_msg(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await state.update_data(date=message.text)
	if data.get('edit', False) == False:
		await message.answer(text='3. Напишите, какие работы были проведены *написать необходимо одним сообщением')
		await state.set_state(CheckState.get_works_type.state)
	else:
		await get_check_info(message, state)

async def pick_work(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await state.update_data(workstype=message.text)
	await message.answer(text='4. Какие реагенты и материалы были привезены на объект')
	if data.get('edit', False) == False:
		await state.set_state(CheckState.get_reagents.state)
	else:
		pass


async def get_reagents(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await state.update_data(reagents=message.text)
	await message.answer(text='5. Напишите суммы оплаты, которую вы получили на руки')
	if data.get('edit', False) == False:
		await state.set_state(CheckState.get_payment.state)
	else:
		pass

async def get_payment(message: types.Message, state: FSMContext):
	data = await state.get_data()
	await state.update_data(payment=message.text)
	if data.get('edit', False) == False:
		await get_check_info(message, state)
	else:
		pass




async def get_check_info(message: types.Message, state: FSMContext):
	data = await state.get_data()
	msg = await work.check.get_check_data(data, message.chat.id)
	await state.set_state(CheckState.check_info.state)
	await message.answer(text=msg, reply_markup=keyboards.edit_check)
	await state.update_data(edit = False)

async def edit_check(callback: types.CallbackQuery, state: FSMContext):
	chengable = callback.data.split('_')[2]
	await state.update_data(edit = True)
	await state.update_data(chengable = chengable)
	if chengable == 'object':
		await objects_show(callback, state)
		await callback.answer()
		return
	elif chengable == 'date':
		await callback.answer()
		await state.set_state(CheckState.get_date.state)
		await callback.message.edit_text('Введите новую дату', reply_markup=keyboards.current_time)
		return
	await callback.message.edit_text(text='Введите новое значение')

	await callback.answer()
	await state.set_state(CheckState.editor.state)

async def edit_msg(message: types.Message, state: FSMContext):
	data = await state.get_data()
	chengable = data['chengable']
	data[chengable] = message.text
	await state.set_data(data)
	await get_check_info(message, state)



async def add_to_works(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	data['id'] = callback.message.chat.id
	del data['page']
	del data['edit']
	res = await work.check.add_work(data)
	msg = 'Спасибо! Данные записал.'
	if res == False:
		msg = 'Внимание! Произошла ошибка!'
	await callback.message.edit_text(msg)
	await asyncio.sleep(2)
	await menu(callback.message, state)
def register_handlers_client(dp: Dispatcher):

	dp.register_callback_query_handler(check_begin, state=MenuState.in_menu, text='work_check')
	dp.register_callback_query_handler(next_object, state= CheckState.object_name_pick, text='next')
	dp.register_callback_query_handler(prev_object, state= CheckState.object_name_pick, text='prev')
	dp.register_callback_query_handler(add_object, state= CheckState.object_name_pick, text='check_add')
	dp.register_message_handler(get_object_name, state = ObjectsAdd.name_pending)
	dp.register_callback_query_handler(objects_show, state = ObjectsAdd.name_pending, text = 'back')
	dp.register_callback_query_handler(menu_call, state=CheckState.object_name_pick, text='back')
	dp.register_callback_query_handler(delete_object, state = CheckState.get_date, text = 'check_delete_project')


	dp.register_callback_query_handler(pick_object, state=CheckState.object_name_pick, text_startswith = 'pick_work_object_')
	dp.register_callback_query_handler(pick_date, state=CheckState.get_date, text_startswith = 'pick_current_time')
	dp.register_message_handler(pick_date_msg, state=CheckState.get_date)
	dp.register_message_handler(pick_work, state=CheckState.get_works_type)
	dp.register_message_handler(get_reagents, state=CheckState.get_reagents)
	dp.register_message_handler(get_payment, state=CheckState.get_payment)
	dp.register_message_handler(get_check_info, state = CheckState.check_info)
	dp.register_callback_query_handler(edit_check, state=CheckState.check_info, text_startswith ='check_edit_')
	dp.register_message_handler(edit_msg, state=CheckState.editor)
	dp.register_callback_query_handler(add_to_works, state = CheckState.check_info, text='check_accpet')




