import datetime
import pytz

from create import pass_to_work


async def pass_correct(password):#todo подумать о том чтобы сделать пароль в бд
	return pass_to_work == password

async def get_cur_time():
	cur_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
	cur_time = cur_time.strftime('%Y-%m-%d %H:%M')
	return cur_time



