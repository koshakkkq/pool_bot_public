from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import work.users as users
from work.utils import pass_correct
from utils.phone import phone_to_normal
import work.keyboards as keyboards
from work.handlers.menu import menu
from create import super_admin_id

class WorkGreetingStates(StatesGroup):
	password_pending = State()
	phone_pending = State()


async def greetings_password(message: types.Message, state:FSMContext):
	if await users.cur_status(message.chat.id) > 0:#направление в меню
		await menu(message, state)
		return
	await message.answer('🤖 Введите пожалуйста пароль.')
	await state.set_state(WorkGreetingStates.password_pending.state)
	await state.reset_data()


async def get_password(message: types.Message, state: FSMContext):
	password = message.text
	if await pass_correct(password):
		await users.pass_entered(message.chat.id)
		await correct_pass(message, state)
	else:
		await wrong_pass(message, state)


async def correct_pass(message:types.Message, state: FSMContext):
	await state.set_state(WorkGreetingStates.phone_pending.state)
	await message.answer('Поделитесь номером 📞', reply_markup=keyboards.contact_request)


async def wrong_pass(message:types.Message, state: FSMContext):
	await message.answer('❌Пароль не верный, попробуйте еще раз')


async def get_contact(message: types.Message, state: FSMContext):
		phone_number = await phone_to_normal(message.contact['phone_number'])
		res = await users.update_by_phone(phone_number, message.chat.id)
		if res == True:
			res = await users.get_lvl(message.chat.id)
			if res > 0:
				await menu(message, state)
				return
			else:
				await message.answer(f'❌ У вас нет доступа к этой функции \n\nНапишите [администратору](tg://user?id={super_admin_id})', parse_mode='MarkdownV2')
				return
		else:
			await message.answer(
				'Ошибка не сервере! Попробуйте ещё раз')
			await greetings_password(message, state)
		return

def register_handlers_client(dp: Dispatcher):

	#dp.register_message_handler(greetings_password, state='*', commands=['work'])
	dp.register_message_handler(get_password, state=WorkGreetingStates.password_pending)
	dp.register_message_handler(get_contact, state=WorkGreetingStates.phone_pending, content_types=['contact'])
