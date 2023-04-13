import logging

from create import db_project

users = db_project.users
clients = db_project.clients
async def get_client_phone_by_id(id):
	try:
		res = await clients.find_one({'id': id})
		return res['phone']
	except Exception as e:
		raise e

async def is_client(id):
	try:
		res = await clients.count_documents({'id':id})
		return res != 0
	except Exception as e:
		logging.error(e)
		return False


async def get_lvl(id):
	try:
		res = await users.find_one({'id':id})
		if res == None:
			return 0
		return res.get('lvl', 0)
	except Exception as e:
		logging.error(e)
		return False


async def update_by_phone(phone, id):
	try:
		await users.update_one({'phone':phone}, {'$set':{'id':id}})
		await clients.update_one({'phone':phone}, {'$set':{'id':id}})
		return True
	except Exception as e:
		logging.error(e)
		return False

