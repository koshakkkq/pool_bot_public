import logging
import os

from create import db_work
from work.utils import get_cur_time
import pandas as pd
import datetime
import time
import pytz
import asyncio

works = db_work.works


async def unpack_dir(dir):
	for i in dir['user_description'][0]:
		dir[i] = dir['user_description'][0][i]
	del dir['user_description']
	del dir['_id']


def to_csv_wrapper(df, path):
	df.to_csv(path, sep=';', encoding='cp1251')

async def get_review_file(chat_id, msg_id):
	try:
		cur_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).timestamp()
		time_to_find = cur_time - (30 * 24 * 60 * 60) - 60 * 60
		pipeline = [
			{'$match':
				{'timestamp':
					{
						'$gt': time_to_find
					}
				}
			},
			{'$lookup':
				{
					'from': "users_description",
					'localField': "id",
					'foreignField': "id",
					'as': "user_description"
				}
			}]
		docs = {'object': [],  # оьъект
				'date': [],  # дата
				'workstype': [],  # комментарий
				'reagents': [],  # реагенты
				'payment': [],  # оплата
				'name': [],  # Имя работника
				'number': [],  # Табельный номер
				'phone': [],  # Номер телефона
				'position': []  #Должность
				}
		async for doc in works.aggregate(pipeline):
			await unpack_dir(doc)
			for i in doc:
				if docs.get(i, None) is None:
					continue
				docs[i].append(doc[i])
		df = pd.DataFrame(docs)
		loop = asyncio.get_event_loop()
		df = df.rename(columns = {'object': 'Объект',
				'date': 'Дата',
				'workstype': 'Комментарий',
				'reagents':  'Реагенты',
				'payment':   'Оплата',
				'name':      'Имя работника',
				'number':    'Табельный номер',
				'phone':     'Номер телефона',
				'position':  'Должность'}, errors='raise')
		dt = int(time.time())
		fileName = f'temp/{dt}_{chat_id}_{msg_id}.csv'
		await loop.run_in_executor(None, to_csv_wrapper, df, fileName)
		return fileName
	except Exception as e:
		logging.error(e)
		return None


async def delete_review(path):
	try:
		loop = asyncio.get_event_loop()
		await loop.run_in_executor(None, os.remove, path)
	except Exception as e:
		logging.error(e)
		return None
