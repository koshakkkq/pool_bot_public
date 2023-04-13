from aiogram import Dispatcher

from shop.handlers.greeting import first_msg_menu, menu_msg, about_msg, reviews_msg
from shop.handlers.services import our_services_begin_msg
from shop.handlers.works import our_works_begin_msg
from shop.handlers.consultation import consultation_begin_msg
from shop.handlers.store import categories_msg
def register_commands(dp: Dispatcher):

	dp.register_message_handler(first_msg_menu, state = "*", commands = ['start'])
	dp.register_message_handler(menu_msg, state = "*", commands= ['menu'])
	dp.register_message_handler(consultation_begin_msg, state="*", commands=['zayavka'])
	dp.register_message_handler(categories_msg, state = "*", commands = ['zakaz'])
	dp.register_message_handler(about_msg, state="*", commands=['info'])
	dp.register_message_handler(our_works_begin_msg, state="*", commands=['raboti'])
	dp.register_message_handler(our_services_begin_msg, state = "*", commands=['uslugi'])
	dp.register_message_handler(reviews_msg, state = "*", commands=['otzivy'])
	#dp.register_message_handler(reviews_msg, state = "*", commands=['help'])

