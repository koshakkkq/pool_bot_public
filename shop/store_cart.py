import datetime
import logging

import bson

from create import db_shop, bot, channel_id
from shop.currency import get_price_in_rub


cart = db_shop.cart

async def add_to_cart(user_id, product_id, count):
	try:
		product_id = bson.ObjectId(product_id)
	except Exception as e:
		logging.error(e)
		return False
	cur_time = datetime.datetime.now(datetime.timezone.utc)
	try:
		await cart.update_many({'user_id': user_id}, {'$set':{'last_update': cur_time}})
	except Exception as e:
		logging.error(e)
		return False

	try:
		await cart.update_many({'user_id': user_id,'product_id': product_id}, {'$set':{'count':count, 'last_update':cur_time},
																			   '$setOnInsert':{'user_id': user_id,'product_id': product_id}},
							   													upsert=True)
	except Exception as e:
		logging.error(e)
		return False
	return True

async def get_msg_products_in_cart(user_id):
	msg = ''
	sum = 0
	try:
		cursor = cart.aggregate([{
		"$lookup":{
			"from":"products",
			"localField":"product_id",
			"foreignField":"_id",
			"as": "product"
			}
		}, {"$match":{"user_id":user_id}}])
	except Exception as e:
		logging.error(e)
		return ''

	try:
		for document in await cursor.to_list(None):
			try:
				price_in_rub = await get_price_in_rub(document['product'][0]['currency'], document['product'][0]['price'])
				msg += f"{document['product'][0]['name']}: {price_in_rub} x {document['count']} = {price_in_rub*document['count']}\n\n"
				sum += price_in_rub*document['count']
			except Exception as e:
				logging.error(e)
				continue
		msg += f"Сумма: {sum}"
		return msg
	except Exception as e:
		logging.error(e)
		return ''


async def get_products_in_cart(user_id):
	try:
		cursor = cart.aggregate([{
		"$lookup":{
			"from":"products",
			"localField":"product_id",
			"foreignField":"_id",
			"as": "product"
			}
		}, {"$match":{"user_id":user_id}}])
	except Exception as e:
		logging.error(e)
		return []
	res = []
	try:
		for document in await cursor.to_list(None):
			try:
				res.append({"name":document['product'][0]['name'], "cnt":document['count'], 'id': str(document['_id'])})
			except Exception as e:
				logging.error(e)
				continue
		return res
	except Exception as e:
		logging.error(e)
		return []

async def get_product_cnt(user_id, cart_product_id):
	try:
		cart_product_id = bson.ObjectId(cart_product_id)
	except Exception as e:
		logging.error(e)
		return 1
	try:
		res = await cart.find_one({'user_id':user_id, '_id': cart_product_id})
		return res.get('count', 1)
	except Exception as e:
		logging.error(e)
		return 1

async def get_product_id(user_id, cart_product_id):
	try:
		cart_product_id = bson.ObjectId(cart_product_id)
	except Exception as e:
		logging.error(e)
		return None
	try:
		res = await cart.find_one({'user_id':user_id, '_id': cart_product_id})
		return res.get('product_id', None)
	except Exception as e:
		logging.error(e)
		return None


async def delete_product(user_id, cart_product_id):
	try:
		cart_product_id = bson.ObjectId(cart_product_id)
	except Exception as e:
		logging.error(e)
		return None

	try:
		await cart.delete_one({'user_id':user_id, '_id': cart_product_id})
		return True
	except Exception as e:
		logging.error(e)
		return False


async def update_cart(user_id, cart_product_id, cnt):
	try:
		res = await get_product_id(user_id, cart_product_id)
		if res == None:
			raise 'None product_id'
		res = await add_to_cart(user_id, res, cnt)
		return res
	except Exception as e:
		logging.error(e)
		return False


async def delete_all_cart(user_id):
	try:
		await cart.delete_many({"user_id":user_id})
	except Exception as e:
		raise e

async def order(phone,user_id, comm_type):
	try:
		cart_msg = await get_msg_products_in_cart(user_id)
		if cart_msg == 'Сумма: 0':
			return False
		msg = f'Заказ:\nТелефон: {phone}\nУдобнее общаться в: {comm_type}\n\nТовары:\n{cart_msg}'
		await delete_all_cart(user_id)
		await bot.send_message(chat_id=channel_id, text=msg)

		return True
	except Exception as e:
		logging.error(e)
		return False