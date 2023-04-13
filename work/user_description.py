import asyncio

import bson

from create import db_work
from work.users import get_phone_by_id, update_phone
from utils.phone import phone_to_normal
import logging

users_description = db_work.users_description

async def get_description(id):

	try:
		phone = await get_phone_by_id(id)
		data = await users_description.find_one_and_update({'id': id},
														   {'$setOnInsert': {'id': id, 'name': None,
																			 'phone': phone,
																			 'number': None, 'position': None}},
														   upsert=True)
		if data is None:
			return {'id': id, 'name': None,'phone': phone,'number': None, 'position': None}
		return data
	except Exception as e:
		logging.error(e)
		return None


async def get_description_msg(id):
	try:
		data = await get_description(id)
		msg = f'Добро пожаловать в ваш профиль:\n\n Ваше ФИО: {str(data["name"])}\nВаш номер телефона: {str(data["phone"])}\n' \
			  f'Ваш табельный номер: {str(data["number"])}\nВаша должность: {str(data["position"])}\n\n' \
			  f'Выберите какую информацию вы хотите поменять.'
		return msg
	except Exception as e:
		logging.error(e)
		return None

async def get_name(id):
	try:
		res = await users_description.find_one({'id':id})
		return res.get('name', '')
	except Exception as e:
		logging.error(e)
		return ''

async def is_description_full(id):
	try:
		res = await users_description.find_one({'id':id})
		if res == None:
			return False
		for i in res:
			if res[i] is None:
				return False
		return True
	except Exception as e:
		logging.error(e)
		return False


async def update_description(id, index, val):
	try:
		if index == 'phone':
			val = await phone_to_normal(val)
		update_data = {index:val}
		await users_description.update_one({'id':id}, {'$set':update_data})
		if index == 'phone':
			await update_phone(id, val)
	except Exception as e:
		logging.error(e)
		return None


