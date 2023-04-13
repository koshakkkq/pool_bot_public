import datetime
import io
import logging
import sys

import aiogram.types
import pytz

from create import web_dav_client, bot, upload_chat_id
import project.projects as projects
import asyncio

from io import BytesIO, BufferedReader

async def add_dir(dir_name):
	try:
		loop = asyncio.get_event_loop()
		await loop.run_in_executor(None, web_dav_client.mkdir, dir_name)
		return
	except Exception as e:
		logging.error(e)
		raise e

def get_file_format(path:str):
	return path.split('.')[-1]


async def init_dir_for_project(dir_name):
	try:
		if await dir_exist(dir_name) == True:
			return True
		await add_dir(dir_name)
		return False
	except Exception as e:
		logging.error(e)
		raise e

async def add_file(file_id, project_id, file_type):
	try:
		if file_id == None:
			raise 'file_id is NoneType'

		if project_id == None:
			raise 'project_id is NoneType'

		file_name = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
		file_name = file_name.strftime('Дата_%Y-%m-%d, Время_%H-%M-%S.%f')
		project_dir = await projects.get_project_dir(project_id)

		path = f'{project_dir}/'
		if file_type == 'video':
			await bot.send_video(chat_id=upload_chat_id, video=file_id, caption=f'{path}{file_name}')
		else:
			await bot.send_photo(chat_id=upload_chat_id, photo=file_id, caption=f'{path}{file_name}')
	except Exception as e:
		logging.error(e)
		return False

async def add_text(text, project_id):
	try:
		if text == None or text == "":
			raise 'file_id is empty'

		if project_id == None:
			raise 'project_id is NoneType'

		file = io.BytesIO(str.encode(text))
		project_dir = await projects.get_project_dir(project_id)

		ext = 'txt'
		file_name = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
		file_name = file_name.strftime('Дата_%Y-%m-%d, Время_%H-%M-%S.%f')

		res = await dir_exist(project_dir)
		if res == False:
			await add_dir(project_dir)

		path = f'{project_dir}/'


		await _add_file_from_object(file, f'{path}{file_name}.{ext}')
		return True
	except Exception as e:
		logging.error(e)
		return False

async def _add_file_from_object(file_obj, file_path):
	try:
		loop = asyncio.get_event_loop()
		await loop.run_in_executor(None, web_dav_client.upload_to, file_obj,file_path)
	except Exception as e:
		raise e



async def dir_exist(dirName):
	try:
		loop = asyncio.get_event_loop()
		res = await loop.run_in_executor(None,  web_dav_client.check, f'{dirName}/')
		return res
	except Exception as e:
		raise e