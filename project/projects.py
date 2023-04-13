import logging

import bson
from pymongo.errors import DuplicateKeyError
import project.web_dav_projects as web_dav
from create import db_project
import project.web_dav_projects
projects = db_project.projects
mail = db_project.mail
subscriptions = db_project.subscriptions
can_subscribe = db_project.can_subscribe

async def get_projects(skipped):
	try:
		cursor = projects.find({}).sort("name")
		cur = 0
		docs = []
		for document in await cursor.to_list(length=10000):
			if skipped != 0:
				skipped -= 1
				continue
			docs.append({'id': str(document['_id']), 'name': document['name']})
			cur += 1
			if cur == 6:
				break
		return docs
	except Exception as e:
		logging.error(e)
		return None

async def get_project_cnt():
	try:
		cnt = await projects.count_documents({})
		return cnt
	except Exception as e:
		logging.error(e)
		return 0


async def add_project(name, dir_name):
	try:
		await projects.insert_one({'name':name, 'dir': dir_name})
		res = await web_dav.init_dir_for_project(dir_name)
		if res == True:
			return "Duplicate_dir"
		return None
	except DuplicateKeyError as e:
		return "Duplicate_name"
	except Exception as e:
		logging.error(e)
		return "Err"


async def update_project_dir(project_id, dir_name):
	try:
		await projects.update_one({'_id':bson.ObjectId(project_id)}, {'$set':{'dir': dir_name}})
		res = await web_dav.init_dir_for_project(dir_name)
		if res == True:
			return "Duplicate_dir"
		return None
	except Exception as e:
		logging.error(e)
		return "Err"


async def delete_project(id):
	try:
		await mail.delete_many({'project_id':bson.ObjectId(id)})
		await can_subscribe.delete_many({'project_id':bson.ObjectId(id)})
		await subscriptions.delete_many({'project_id':bson.ObjectId(id)})
		await projects.delete_one({'_id':bson.ObjectId(id)})
		return True
	except Exception as e:
		logging.error(e)
		return False

async def get_project_name(id):
	try:
		res = await projects.find_one({'_id':bson.ObjectId(id)})
		if res == None:
			return None
		return res.get('name', None)
	except Exception as e:
		logging.error(e)
		return None


async def get_project_dir(id):
	try:
		res = await projects.find_one({'_id':bson.ObjectId(id)})
		if res == None:
			raise 'id NoneType in get_project_dir'
		return res.get('dir', None)
	except Exception as e:
		raise e
