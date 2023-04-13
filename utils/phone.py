async def phone_to_normal(phone:str):
	phone = list(phone)
	if phone[0] != '+':
		phone.insert(0, '+')
	phone = [i for i in phone if i != '(' and i != ')' and i != ' ']
	return ''.join(phone)
