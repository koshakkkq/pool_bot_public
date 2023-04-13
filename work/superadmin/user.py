from create import db_work, db_project
import logging

users = db_work.users
users_project = db_project.users
clients = db_project.clients
subscriptions = db_project.subscriptions
can_subscribe = db_project.can_subscribe

async def add(user_lvl, phone):
	try:
		users.update_one({'phone':phone},{'$setOnInsert':{'id':None, 'entered_pass':False}, '$set':{'lvl':user_lvl}} ,upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def add_user_to_project(phone, user_lvl):
	try:
		res = await delete_client(phone)
		if res == False:
			return False

		await users_project.update_one({'phone':phone},{'$setOnInsert':{'id':None}, '$set':{'lvl':user_lvl}} ,upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def add_client(phone):
	try:
		res = await delete_user_from_project(phone)
		if res == False:
			return False
		await clients.update_one({'phone': phone}, {'$setOnInsert': {'id': None}},upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete(phone):
	try:
		await delete_mailing(phone)
		await users.delete_one({'phone':phone})
		await delete_user_from_project(phone)
		await delete_client(phone)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete_user_from_project(phone):
	try:
		await users_project.delete_one({'phone':phone})
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete_client(phone):
	try:
		await clients.delete_one({'phone':phone})
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete_by_id(id):
	try:
		id = int(id)
		await users.delete_one({'id':id})
		await delete_user_by_id(id)
		await delete_client_by_id(id)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete_user_by_id(id):
	try:
		await users_project.delete_one({'id':id})
		return True
	except Exception as e:
		logging.error(e)
		return False


async def delete_client_by_id(id):
	try:
		await clients.delete_one({'id':id})
		return True
	except Exception as e:
		logging.error(e)
		return False
async def user_cur_status(id):
	try:
		res = await users.find_one({'id':id})
		return res
	except Exception as e:
		logging.error(e)
		return None

async def update_by_phone(phone, id):
	try:
		await users.update_one({'phone':phone},{'$setOnInsert':{'lvl':0}, '$set':{'phone':phone, 'id':id}}, upsert=True)
		return
	except Exception as e:
		logging.error(e)
		return None

async def is_exist(id):
	try:
		res = await users.count_documents({'id':id})
		return res != 0
	except Exception as e:
		logging.error(e)
		return False


async def get_client_by_phone(phone):
	try:
		res = await clients.find_one({'phone':phone})
		return res.get('id', None)
	except Exception as e:
		logging.error(e)
		return None


async def get_user_by_phone(phone):
	try:
		res = await users_project.find_one({'phone':phone})
		return res.get('id', None)
	except Exception as e:
		logging.error(e)
		return None
async def delete_mailing(phone):
	try:
		id = await get_client_by_phone(phone)
		if id == None:
			return True
		await subscriptions.delete_many({'user_id':id})
	except Exception as e:
		logging.error(e)
		return False
