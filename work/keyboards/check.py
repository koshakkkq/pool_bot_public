from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from work import check
from work.users import get_lvl

keyboard1 = [[InlineKeyboardButton('Назад', callback_data='back')]]
back = InlineKeyboardMarkup(inline_keyboard=keyboard1)





edit_check = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton('Объект', callback_data='check_edit_object'), InlineKeyboardButton('Дата / Время', callback_data='check_edit_date')],
												   [InlineKeyboardButton('Комментарий', callback_data='check_edit_workstype'), InlineKeyboardButton('Реагенты', callback_data='check_edit_reagents')],
												   [InlineKeyboardButton('Сумма оплаты', callback_data='check_edit_payment')],
												   [InlineKeyboardButton('✅ Все верно!', callback_data='check_accpet')]])
async def get_objects_keyboard(page, id):

	lvl = await get_lvl(id)

	objects = await check.get_objects((page-1)*6)
	objects_cnt = await check.get_object_cnt()
	objects_btns = []

	for i in range(0, len(objects), 2):
		if i + 1 < len(objects):
			objects_btns.append([InlineKeyboardButton(text=objects[i]['name'], callback_data=f'pick_work_object_{objects[i]["id"]}'), InlineKeyboardButton(text=objects[i+1]['name'], callback_data=f'pick_work_object_{objects[i+1]["id"]}')])
		else:
			objects_btns.append([InlineKeyboardButton(text=objects[i]['name'], callback_data=f'pick_work_object_{objects[i]["id"]}')])

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

	inline_btn_3 = InlineKeyboardButton('Назад', callback_data='back')
	objects_btns.append([inline_btn_3])

	if lvl >= 2:
		inline_btn_3 = InlineKeyboardButton('Добавить➕', callback_data='check_add')
		objects_btns.append([inline_btn_3])
	return InlineKeyboardMarkup(inline_keyboard=objects_btns)



async def get_time_keyboard(id):
	lvl = await get_lvl(id)

	keyboard1 = [[InlineKeyboardButton('Установить текущее', callback_data='pick_current_time')]]

	if lvl >= 2:
		keyboard1.append([InlineKeyboardButton('Удалить❌', callback_data='check_delete_project')])
	return InlineKeyboardMarkup(inline_keyboard=keyboard1)
