import datetime
import time
import pytz

from create import db_work
from work.user_description import get_name
from bson.objectid import ObjectId
import logging

objects = db_work.objects
works = db_work.works

async def get_objects(skipped):
	try:
		cursor = objects.find({}).sort('name')
		cur = 0
		docs = []
		for document in await cursor.to_list(length=10000):
			if skipped != 0:
				skipped -= 1
				continue
			docs.append({'id':str(document['_id']), 'name':document['name']})
			cur += 1
			if cur == 6:
				break
		return docs
	except Exception as e:
		logging.error(e)
		return None


async def get_object_cnt():
	try:
		cnt = await objects.count_documents({})
		return cnt
	except Exception as e:
		logging.error(e)
		return 0


async def add_object(name):
	try:
		await objects.insert_one({'name':name})
		return True
	except Exception as e:
		logging.error(e)
		return False



async def get_object_name(id):
	try:
		res = await objects.find_one({'_id':ObjectId(id)})
		return res.get('name', '')
	except Exception as e:
		logging.error(e)
		return ''

async def get_check_data(dir, id):
	return f'{await get_name(id)} Вы ввели данные верно?\n\n' \
		   f'1.📍Объект: {dir["object"]}\n' \
		   f'2.📅 Дата/Время: {dir["date"]}\n' \
		   f'3.📝 Комментарий: {dir["workstype"]}\n' \
		   f'4.⚒ Реагенты и материалы: {dir["reagents"]}\n' \
		   f'5.💰 Сумма оплаты: {dir["payment"]}\n' \
		   f'Выберите пункт, который хотите отредактировать'


async def add_work(dir):
	try:
		dir['timestamp'] = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).timestamp())
		await works.insert_one(dir)
		return True
	except Exception as e:
		logging.error(e)
		return False

async def delete_object(object_id):
	try:
		await objects.delete_one({'_id':ObjectId(object_id)})
		return True
	except Exception as e:
		logging.error(e)
		return False