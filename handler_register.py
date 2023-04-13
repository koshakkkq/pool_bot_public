from aiogram import Dispatcher, types
from create import bot
import work.handlers.greeting
import work.superadmin.handlers.handlers
import project.handlers.greeting
import shop.handlers.greeting
import shop
import project
import work
import shop


async def get_channel_id(message: types.Message):
	await message.answer(message.chat.id)

async def get_photo_id(message:types.Message):
	#print(f'"{message.video.file_id}",')
	print(f'"{message.photo[-1].file_id}",')
def register_handlers(dp: Dispatcher):
	dp.register_channel_post_handler(get_channel_id, state= '*', text='/get_id')

	#dp.register_message_handler(get_photo_id, state='*', content_types=['photo'])
	shop.register_commands(dp)
	dp.register_message_handler(work.superadmin.handlers.handlers.menu, state='*', commands=['admin'])
	dp.register_message_handler(work.handlers.greeting.greetings_password, state='*', commands=['work'])
	dp.register_message_handler(project.handlers.greeting.greetings, state='*', commands=['project'])
	shop.register_handlers(dp)
	work.register_handlers(dp)
	project.register_handlers(dp)