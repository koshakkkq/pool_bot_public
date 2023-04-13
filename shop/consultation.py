from create import bot, channel_id
async def send_to_chanel(name: str, communication_type: str, question: str, phone:str, username: str, id):
	if name is None:
		raise "empty name"
	if communication_type is None:
		raise "empty communication_type"
	if question is None:
		raise "empty question"
	if phone is None:
		raise "empty phone"
	if username == None:
		username = 'Не указан'

	msg = f'Консультация\nИмя: {name}\nУдобнее общаться в: {communication_type}\nUsername: {username}\nНомер телефона :{phone}\nВопрос: {question}\n[Написать](tg://user?id={id})'
	await bot.send_message(chat_id=channel_id, text=msg, parse_mode='Markdown')
