from create import db_work
from create import db_project
import logging

users = db_work.users
users_project = db_project.users
async def cur_status(id):
	try:
		res = await users.find_one({'id':id})
		if res == None:
			return 0
		if res.get('entered_pass', False) is False:
			return 0
		return int(res.get('lvl', 0))
	except Exception as e:
		logging.error(e)
		return 0

async def cur_status_by_phone(phone):
	try:
		res = await users.find_one({'phone': phone})
		if res == None:
			return 0
		return res['lvl']
	except Exception as e:
		logging.error(e)
		return 0


async def update_phone(id, phone):
	try:
		await users.update_one({'id':id}, {'$set':{'phone':phone}}, upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def update_by_phone(phone, id):
	try:
		await users.update_one({'phone':phone}, {'$set':{'id':id, 'entered_pass': True}, '$setOnInsert':{'lvl':0}}, upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False


async def get_phone_by_id(id):
	try:
		res = await users.find_one({'id': id})
		return res.get('phone', None)
	except Exception as e:
		logging.error(e)
		return None

async def get_lvl(id):
	try:
		res = await users.find_one({'id': id})
		if res == None:
			return 0
		lvl = res.get('lvl', 0)
		return int(lvl)
	except Exception as e:
		logging.error(e)
		return 0


async def pass_entered(id):
	try:
		await users.update_one({'id':id}, {'$set':{'entered_pass':True}})
		return True
	except Exception as e:
		logging.error(e)
		return False

