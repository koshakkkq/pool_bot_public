from aiogram import Dispatcher

import work.superadmin.handlers.handlers
import work.handlers
import work.handlers.greeting as greeting_handler
import work.superadmin.handlers.handlers as superadmin_handlers

def register_handlers(dp: Dispatcher):

	work.handlers.greeting.register_handlers_client(dp)
	work.handlers.menu.register_handlers_client(dp)
	work.handlers.account.register_handlers_client(dp)
	work.handlers.check.register_handlers_client(dp)

	work.superadmin.handlers.handlers.register_handlers_client(dp)