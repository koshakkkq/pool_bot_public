from aiogram import Dispatcher

import shop.handlers.greeting
import shop.handlers.services
import shop.handlers.works
import shop.handlers.consultation
import shop.handlers.store
import shop.handlers.cart

def register_handlers(dp: Dispatcher):
	shop.handlers.greeting.register_handlers(dp)
	shop.handlers.services.register_handlers(dp)
	shop.handlers.works.register_handlers(dp)
	shop.handlers.consultation.register_handlers(dp)
	shop.handlers.cart.register_handlers(dp)
	shop.handlers.store.register_handlers(dp)
