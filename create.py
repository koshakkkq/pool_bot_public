from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
from utils.config import parse_config
from webdav3.client import Client

config = parse_config()

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')


API_TOKEN = config['tg_token']

db_work = client.work
db_project = client.project
db_shop = client.shop

super_admin_id = config['super_admin_id']

pass_to_work = config['pass_to_work']

upload_chat_id = config['upload_chat_id']

web_dav_client_data = {
 'webdav_hostname': config['webdav_hostname'],
 'webdav_login':     config['webdav_login'],
 'webdav_password':  config['webdav_password'],
 'webdav_timeout':300}

web_dav_client = Client(web_dav_client_data)

channel_id = config['channel_id']
picture_base_url = config['picture_server_base']

eur_price = 1

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
