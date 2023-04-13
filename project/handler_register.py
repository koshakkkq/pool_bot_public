from aiogram import Dispatcher
from project.handlers.greeting import register_handlers_client as register_greetings
from project.employee.handlers import register_handlers_client as register_employee

from project.client_handlers.handlers import register_handlers_client as register_client
def register_handlers(dp: Dispatcher):
	register_greetings(dp)
	register_employee(dp)
	register_client(dp)