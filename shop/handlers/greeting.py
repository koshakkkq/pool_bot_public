import asyncio
import logging

from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from shop.photos import photos
from shop.stickers import stickers
import shop.keyboards.greeting as keyboards
from create import bot
async def first_msg_menu(message: types.Message, state:FSMContext):
	await state.reset_data()

	#res = await message.answer_sticker(sticker=stickers["first_msg"], disable_notification=True)
	#await state.update_data(delete_msg=res.message_id)
	await asyncio.sleep(0.02)
	await message.answer_photo(photo=photos["greeting_menu"], caption=f'Добрый день "{message.from_user.first_name}" ☀\nВас приветствует Магазин бассейнов №1.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nЗдесь вы сможете посмотреть всю необходимую информацию, посмотреть наши проекты и созвониться с нашим сотрудником. 👇🏼',
						 reply_markup=keyboards.menu_keyboard)


async def about(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)
	await callback.message.delete()
	await callback.message.answer_photo(photo=photos["about"], caption='Магазин бассейнов No1 более 10 лет на рынке, монтажа и изготовления бассейнов в Ростовской области.\nВ наших силах построить любой бассейн от небольших частных дизайнерских, до общественных бассейнов.\n\nНаша главная задача – это качественно выполнить все работы. Наши специалисты соблюдают все сроки, заранее согласованные с клиентом. Благодаря нашему опыту мы знаем все профессиональные тонкости, которые необходимые для создание бассейна Вашей мечты!',
										reply_markup=keyboards.about_keyboard)
	await callback.answer()


async def about_msg(message: types.Message, state:FSMContext):

	await state.reset_data()
	await message.answer_photo(photo=photos["about"],
										caption='Магазин бассейнов No1 более 10 лет на рынке, монтажа и изготовления бассейнов в Ростовской области.\nВ наших силах построить любой бассейн от небольших частных дизайнерских, до общественных бассейнов.\n\nНаша главная задача – это качественно выполнить все работы. Наши специалисты соблюдают все сроки, заранее согласованные с клиентом. Благодаря нашему опыту мы знаем все профессиональные тонкости, которые необходимые для создание бассейна Вашей мечты!',
										reply_markup=keyboards.about_keyboard)


async def client_menu(callback: types.CallbackQuery, state: FSMContext):
	await state.reset_data()

	#res = await callback.message.answer_sticker(sticker=stickers["main_menu"], disable_notification=True)
	#await state.update_data(delete_msg=res.message_id)

	await asyncio.sleep(0.02)

	await callback.message.delete()
	await callback.message.answer(text='☀С возвращением в главное меню Магазина бассейнов №1.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nВыберите интересующий вас пункт меню 👇🏼',
								  reply_markup=keyboards.menu_keyboard)
	await callback.answer()

async def menu_msg(message: types.Message, state:FSMContext):
	await state.reset_data()

	#res = await message.answer_sticker(sticker=stickers["main_menu"], disable_notification=True)
	#await state.update_data(delete_msg=res.message_id)
	await asyncio.sleep(0.02)
	await message.answer(
		text='☀С возвращением в главное меню Магазина бассейнов №1.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nВыберите интересующий вас пункт меню 👇🏼',
		reply_markup=keyboards.menu_keyboard)

async def reviews(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)
	await callback.message.delete()
	await state.reset_data()
	await callback.message.answer(text='❤Почитать наши официальные отзывы вы можете по кнопкам ниже',
								  reply_markup=keyboards.reviews_keyboard)
	await callback.answer()


async def reviews_msg(message: types.Message, state: FSMContext):
	await message.answer(text='❤Почитать наши официальные отзывы вы можете по кнопкам ниже',
								  reply_markup=keyboards.reviews_keyboard)


def register_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(about, state='*', text='shop_about')
	dp.register_callback_query_handler(client_menu, state='*', text = 'shop_main_menu')
	dp.register_callback_query_handler(reviews, state = "*", text = 'shop_reviews')
