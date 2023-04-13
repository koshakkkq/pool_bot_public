import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import project.user as user
import project.keyboards.employee as keyboards
import project.projects as projects
import project.web_dav_projects as web_dav
import project.mailing as mailing
from utils.phone import  phone_to_normal


class ProjectEmployeeStates(StatesGroup):
	in_menu = State()
	in_project = State()
	uploading_file = State()

class AddingProject(StatesGroup):
	pending_name = State()
	pending_dir_name = State()

async def project_menu_msg(message: types.Message, state:FSMContext):
	if await user.get_lvl(message.chat.id) == 0:
		return
	await state.reset_data()
	keyboard = await keyboards.get_objects_keyboard(1, message.chat.id)
	await message.answer('Добро пожаловать в меню проектов.\n\nДля добавления информации выберите проект.', reply_markup=keyboard)
	await state.update_data(page = 1)
	await state.set_state(ProjectEmployeeStates.in_menu.state)

async def project_menu_call(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	await state.reset_data()
	keyboard = await keyboards.get_objects_keyboard(1, callback.message.chat.id)
	await callback.message.answer('Добро пожаловать в меню проектов.\n\nДля добавления информации выберите проект.',
						 reply_markup=keyboard)
	await state.update_data(page=1)
	await state.set_state(ProjectEmployeeStates.in_menu.state)

async def project_menu_print(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	data = await state.get_data()
	keyboard = await keyboards.get_objects_keyboard(data['page'], callback.message.chat.id)
	await callback.message.answer('Добро пожаловать в меню проектов.\n\nДля добавления информации выберите проект.',
						 reply_markup=keyboard)
	await state.set_state(ProjectEmployeeStates.in_menu.state)
async def get_next_project_page(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	data = await state.get_data()
	await state.update_data(page = data['page'] + 1)
	await project_menu_print(callback, state)


async def get_prev_project_page(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	data = await state.get_data()
	await state.update_data(page = data['page'] - 1)
	await project_menu_print(callback, state)




async def add_project_begin(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) < 2:
		return
	await callback.message.edit_text('Введите название проекта', reply_markup=keyboards.back)
	await state.set_state(AddingProject.pending_name.state)

async def add_project_dir_name(message: types.Message, state:FSMContext):
	if await user.get_lvl(message.chat.id) < 2:
		return
	await state.update_data(project_name = message.text)
	await message.answer('Введите название папки в которую будет сохранятся информация, можно привязать к уже существующей папке, для этого введите имя этой папки.\n'
						 '(Вы увидите предупреждение если папка уже существует)', reply_markup=keyboards.back)
	await state.set_state(AddingProject.pending_dir_name.state)

async def add_project_end(message: types.Message, state:FSMContext):
	if await user.get_lvl(message.chat.id) < 2:
		return
	data = await state.get_data()
	dir_name = message.text
	name = data.get('project_name', None)
	if name == None:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await project_menu_msg(message, state)
		return

	res = await projects.add_project(name=name, dir_name=dir_name)
	if res == None:
		await message.answer('Успешно')
		await asyncio.sleep(0.5)
	elif res == 'Err':
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
	elif res == 'Duplicate_name':
		await message.answer('Проект с таким именем уже существует')
		await asyncio.sleep(0.5)
	elif res == 'Duplicate_dir':
		await message.answer('Папка для проекта уже существует! Весь контент будет записан в существующую папку.')
		await asyncio.sleep(0.5)
	await project_menu_msg(message, state)



async def pick_project(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	project_id = callback.data.split('_')[2]
	await state.update_data(project_id = project_id)
	await in_project_menu(callback, state)

async def in_project_menu(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) == 0:
		return
	await state.set_state(ProjectEmployeeStates.in_project.state)
	data = await state.get_data()
	project_name = await projects.get_project_name(data['project_id'])
	keyboard = await keyboards.get_project_keyboard(callback.message.chat.id)
	await callback.message.edit_text(text = f'Добро пожаловать в проект {project_name}\nОтправьте фото/видео или текст отдельным сообщением!', reply_markup=keyboard)
	await callback.answer()


async def in_project_menu_msg(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) == 0:
		return
	await state.set_state(ProjectEmployeeStates.in_project.state)
	data = await state.get_data()
	project_name = await projects.get_project_name(data['project_id'])
	keyboard = await keyboards.get_project_keyboard(message.chat.id)
	await message.answer(text = f'Выберите действие, которое вы хотите совершить с {project_name}\nОтправьте фото/видео или текст отдельным сообщением!', reply_markup=keyboard)

async def get_media(message: types.Message, state: FSMContext, file_id, file_type):
	await state.set_state(ProjectEmployeeStates.uploading_file.state)
	data = await state.get_data()
	project_id = data.get('project_id', None)
	if file_type == 'video':
		res = await mailing.add_mailing(project_id, video_id=file_id)
	else:
		res = await mailing.add_mailing(project_id, photo_id=file_id)


	if res == False:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu_msg(message, state)
		return


	res = await web_dav.add_file(file_id=file_id, project_id=project_id, file_type=file_type)
	if res == False:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu_msg(message, state)
		return
	await message.answer('Файл отправлен для загрузки')
	await in_project_menu_msg(message, state)
	return

async def get_photo(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) == 0:
		return
	await message.answer('Ожидайте обрабатываю!')
	photo = max(message.photo, key=lambda x: x.height)
	file_id = photo.file_id
	await get_media(message, state, file_id, 'photo')

async def get_video(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) == 0:
		return
	await message.answer('Ожидайте обрабатываю!')
	file_id = message.video.file_id
	await get_media(message, state, file_id, 'video')

async def get_text(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) == 0:
		return
	await message.answer('Ожидайте обрабатываю!')
	await state.set_state(ProjectEmployeeStates.uploading_file.state)
	data = await state.get_data()
	project_id = data.get('project_id', None)
	res = await mailing.add_mailing(project_id, text=message.text)
	if res == False:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu_msg(message, state)
		return
	res = await web_dav.add_text(message.text, project_id)
	if res == False:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu_msg(message, state)
		return
	await message.answer('Успешно')
	await in_project_menu_msg(message, state)

class UpdatingProject(StatesGroup):
	pending_new_dir_name = State()


async def delete_project(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) < 2:
		return
	data = await state.get_data()
	project_id = data.get('project_id', None)
	if project_id == None:
		await callback.message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await project_menu_call(callback, state)
		return

	res = await projects.delete_project(project_id)
	if res == False:
		await callback.message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await project_menu_call(callback, state)
		return

	await callback.message.answer('Успешно')
	await asyncio.sleep(0.5)
	await project_menu_call(callback, state)


async def update_project_dir(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) < 2:
		return
	await state.set_state(UpdatingProject.pending_new_dir_name.state)
	await callback.message.edit_text('Введите новое название папки',reply_markup=keyboards.back)

async def get_new_dir_name(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) < 2:
		return
	data = await state.get_data()
	project_id = data.get('project_id', None)
	if project_id == None:
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu_msg(message, state)
		return

	res = await projects.update_project_dir(project_id=project_id, dir_name=message.text)
	if res == None:
		await message.answer('Успешно')
		await asyncio.sleep(0.5)
	elif res == 'Err':
		await message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
	elif res == 'Duplicate_dir':
		await message.answer('Папка для проекта уже существует! Весь контент будет записан в существующую папку.')
		await asyncio.sleep(0.5)
	await in_project_menu_msg(message, state)


class AddingClient(StatesGroup):
	pending_phone = State()
	pending_phone_confirm = State()

async def add_client(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) < 2:
		return
	await callback.message.edit_text('Введите номер телефона клиента', reply_markup=keyboards.back)
	await state.set_state(AddingClient.pending_phone.state)

async def add_client_get_phone(message: types.Message, state: FSMContext):
	if await user.get_lvl(message.chat.id) < 2:
		return
	phone = message.text
	phone = await phone_to_normal(phone)
	await state.update_data(client_phone = phone)
	await message.answer(f'Номер приведён в международный формат проверьте: {phone}', reply_markup=keyboards.client_get_phone)
	await state.set_state(AddingClient.pending_phone_confirm.state)


async def accept_phone(callback: types.CallbackQuery, state: FSMContext):
	if await user.get_lvl(callback.message.chat.id) < 2:
		return
	data = await state.get_data()
	phone = data.get('client_phone', None)
	project_id = data.get('project_id', None)
	if phone == None or project_id == None:
		await callback.message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu(callback, state)

	res = await mailing.add_subscriber(phone, project_id)
	if res == False:
		await callback.message.answer('Ошибка на сервере')
		await asyncio.sleep(0.5)
		await in_project_menu(callback, state)

	await callback.message.answer('Успешно')
	await asyncio.sleep(0.5)
	await in_project_menu_msg(callback.message, state)




def register_handlers_client(dp: Dispatcher):

	dp.register_callback_query_handler(get_next_project_page, state=ProjectEmployeeStates.in_menu, text = 'next')
	dp.register_callback_query_handler(get_prev_project_page, state=ProjectEmployeeStates.in_menu, text = 'prev')
	dp.register_callback_query_handler(add_project_begin, state=ProjectEmployeeStates.in_menu, text = 'add')
	dp.register_message_handler(add_project_dir_name, state = AddingProject.pending_name)
	dp.register_message_handler(add_project_end, state= AddingProject.pending_dir_name)
	dp.register_callback_query_handler(project_menu_call, state = AddingProject.pending_name, text = 'back')
	dp.register_callback_query_handler(project_menu_call, state = AddingProject.pending_dir_name, text = 'back')


	dp.register_callback_query_handler(pick_project, state = ProjectEmployeeStates.in_menu, text_startswith= 'pick_project_')

	dp.register_message_handler(get_photo, state =ProjectEmployeeStates.in_project, content_types=['photo'])
	dp.register_message_handler(get_video, state = ProjectEmployeeStates.in_project, content_types=['video'])
	dp.register_message_handler(get_text, state=ProjectEmployeeStates.in_project)
	dp.register_callback_query_handler(project_menu_call, state=ProjectEmployeeStates.in_project, text='back')
	dp.register_callback_query_handler(delete_project, state= ProjectEmployeeStates.in_project, text='project_delete')
	dp.register_callback_query_handler(update_project_dir, state=ProjectEmployeeStates.in_project, text = 'project_change_dir')
	dp.register_message_handler(get_new_dir_name, state = UpdatingProject.pending_new_dir_name)
	dp.register_callback_query_handler(in_project_menu, state = UpdatingProject.pending_new_dir_name, text = 'back')
	dp.register_callback_query_handler(in_project_menu, state = AddingClient.pending_phone, text = 'back')


	dp.register_callback_query_handler(add_client, state=ProjectEmployeeStates.in_project, text = 'add_client')
	dp.register_message_handler(add_client_get_phone, state = AddingClient.pending_phone)
	dp.register_callback_query_handler(accept_phone, state = AddingClient.pending_phone_confirm, text = 'accept_phone')
	dp.register_callback_query_handler(add_client, state = AddingClient.pending_phone_confirm, text = 'decline_phone')