from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
import project.user as user
import project.keyboards.greeting as keyboards
from utils.phone import phone_to_normal
from create import super_admin_id
from project.employee.handlers import project_menu_msg

from project.client_handlers.handlers import client_menu_msg
class projectGreetingStates(StatesGroup):
	phone_pending = State()


async def greetings(message: types.Message, state:FSMContext, from_contact = False):
	if await user.is_client(message.chat.id) == True: #редирект на клиента
		await client_menu_msg(message, state)
		return
	if await user.get_lvl(message.chat.id) != 0: #редирект для сотрудника
		await project_menu_msg(message, state)
		return
	if from_contact == True:
		await message.answer(f'❌ У вас нет доступа к этой функции \n\nНапишите [администратору](tg://user?id={super_admin_id})', parse_mode='MarkdownV2', reply_markup=types.ReplyKeyboardRemove())
		return
	await message.answer("Поделитесь номером 📞", reply_markup=keyboards.contact_request)
	await state.set_state(projectGreetingStates.phone_pending.state)
	await state.reset_data()



async def get_contact(message: types.Message, state: FSMContext):
	phone_number = await phone_to_normal(message.contact['phone_number'])
	res = await user.update_by_phone(phone_number, message.chat.id)
	if res == False:
		await message.answer('Ошибка на сервере! Попробуйте ещё раз')
		await greetings(message, state)
	else:
		await greetings(message, state, True)


def register_handlers_client(dp: Dispatcher):

	dp.register_message_handler(get_contact, state=projectGreetingStates.phone_pending, content_types=['contact'])
