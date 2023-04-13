from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from project import projects
from project.user import get_lvl

keyboard1 = [[InlineKeyboardButton('Назад', callback_data='back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)

keyboard1 = [[InlineKeyboardButton('Верно', callback_data='accept_phone')], [InlineKeyboardButton('Неверно', callback_data='decline_phone')]]
client_get_phone = InlineKeyboardMarkup(inline_keyboard=keyboard1)

async def get_objects_keyboard(page, id):

	lvl = await get_lvl(id)

	objects = await projects.get_projects((page-1)*6)

	objects_cnt = await projects.get_project_cnt()
	objects_btns = []

	for i in range(0, len(objects), 2):
		if i + 1 < len(objects):
			objects_btns.append([InlineKeyboardButton(text=objects[i]['name'], callback_data=f'pick_project_{objects[i]["id"]}'), InlineKeyboardButton(text=objects[i+1]['name'], callback_data=f'pick_project_{objects[i+1]["id"]}')])

		else:
			objects_btns.append([InlineKeyboardButton(text=objects[i]['name'], callback_data=f'pick_project_{objects[i]["id"]}')])

	max_page = (objects_cnt+5)//6
	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data='next')
	btn_back = InlineKeyboardButton('⬅', callback_data='prev')

	if max_page <= 1:
		pass
	elif page == max_page:
		objects_btns.append([btn_back, btn_page_cnt])
	elif page == 1:
		objects_btns.append([btn_page_cnt, btn_forward])
	else:
		objects_btns.append([btn_back, btn_page_cnt, btn_forward])


	if lvl >= 2:
		inline_btn_3 = InlineKeyboardButton('✅ Добавить проект', callback_data='add')
		objects_btns.append([inline_btn_3])
	return InlineKeyboardMarkup(inline_keyboard=objects_btns)


async def get_project_keyboard(id):
	project_menu_arr = []

	lvl = await get_lvl(id)
	if lvl >= 2:
		inline_btn_3 = InlineKeyboardButton('❌Удалить', callback_data='project_delete')
		project_menu_arr.append([inline_btn_3])
		inline_btn_3 = InlineKeyboardButton('🖊️Изменить папку', callback_data='project_change_dir')
		project_menu_arr.append([inline_btn_3])
		inline_btn_3 = InlineKeyboardButton('Добавить заказчика', callback_data='add_client')
		project_menu_arr.append([inline_btn_3])
	project_menu_arr.append([InlineKeyboardButton('↩Назад', callback_data='back')])
	res = InlineKeyboardMarkup(inline_keyboard=project_menu_arr)
	return res
