import datetime

import bson

from create import db_project
from project.user import get_client_phone_by_id
import logging
mail = db_project.mail
can_subscribe = db_project.can_subscribe#todo при удалении проект убирать отсюда проекты
subscribed = db_project.subscriptions

async def add_mailing(project_id, text = None, photo_id = None, video_id = None):
	if project_id == None:
		return
	try:
		await mail.insert_one({'project_id': bson.ObjectId(project_id), 'text':text, 'photo_id':photo_id, 'video_id':video_id, 'created_at': datetime.datetime.now(datetime.timezone.utc)})
		return True
	except Exception as e:
		logging.error(e)
		return False


async def add_subscriber(subscriber_phone, project_id):
	try:
		await can_subscribe.update_one({'phone':subscriber_phone, 'project_id':bson.ObjectId(project_id)}, {'$set': {'phone':subscriber_phone, 'project_id':bson.ObjectId(project_id)}}, upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return False


async def can_subscribe_projects(id):
	try:
		phone = await get_client_phone_by_id(id)
	except Exception as e:
		logging.error(e)
		return None

	try:
		cursor = can_subscribe.aggregate([
		{
		"$lookup":{
			"from":"projects",
			"localField":"project_id",
			"foreignField":"_id",
			"as": "project"
			}
		},
		{"$match":{"phone":phone}}])
		res = []
		for document in await cursor.to_list(length=10000):
			res.append({'name': document['project'][0]['name'], 'id':str(document['project_id']) })
		return res
	except Exception as e:
		logging.error(e)
		return None

async def get_subscribed(id):
	try:
		cursor = subscribed.find({'user_id':id})
		res = []
		for document in await cursor.to_list(length = 10000):
			res.append(str(document['project_id']))
		return res
	except Exception as e:
		logging.error(e)
		return None


async def add_subscribe(user_id, project_id):
	try:
		await subscribed.update_one({'user_id': user_id, 'project_id': bson.ObjectId(project_id)},
									{"$set":{'user_id': user_id, 'project_id': bson.ObjectId(project_id)}},
									   upsert=True)
		return True
	except Exception as e:
		logging.error(e)
		return None


async def delete_subscribe(user_id, project_id):
	try:
		await subscribed.delete_many({'user_id': user_id, 'project_id': bson.ObjectId(project_id)})
		return True
	except Exception as e:
		logging.error(e)
		return None