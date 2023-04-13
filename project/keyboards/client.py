from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from project import projects
from project.mailing import can_subscribe_projects, get_subscribed

def get_sub_symbol(subscribe, subscribed):
	if subscribe in subscribed:
		return '✅'
	else:
		return '❌'


def get_call_data(subscribe, subscribed):
	if subscribe in subscribed:
		return f'cancel_sub_{subscribe}'
	else:
		return f'add_sub_{subscribe}'


async def get_objects_keyboard(id):
	can_subscribe = await can_subscribe_projects(id)
	if can_subscribe == None:
		return None

	subscribed = await get_subscribed(id)

	if subscribed == None:
		return None

	objects_btns = []

	for i in range(0,len(can_subscribe), 2):
		if i + 1 < len(can_subscribe):
			objects_btns.append(
				[InlineKeyboardButton(text=f'{get_sub_symbol(can_subscribe[i]["id"], subscribed)}{can_subscribe[i]["name"]}',
									  callback_data=get_call_data(can_subscribe[i]['id'], subscribed)),
				 InlineKeyboardButton(
					 text=f'{get_sub_symbol(can_subscribe[i+1]["id"], subscribed)}{can_subscribe[i+1]["name"]}',
					 callback_data=get_call_data(can_subscribe[i+1]['id'], subscribed))])
		else:
			objects_btns.append(
				[InlineKeyboardButton(
					text=f'{get_sub_symbol(can_subscribe[i]["id"], subscribed)}{can_subscribe[i]["name"]}',
					callback_data=get_call_data(can_subscribe[i]['id'], subscribed))])


	objects_btns.append([InlineKeyboardButton(text = '🆘 Написать', callback_data = 'admin_info')])

	res = InlineKeyboardMarkup(inline_keyboard=objects_btns)
	return res

