import logging

import bson

from create import db_shop
from shop.currency import get_price_in_rub

categories = db_shop.categories
groups = db_shop.groups
products = db_shop.products


async def get_categories():
	try:
		cursor = categories.find({})
	except Exception as e:
		logging.error(e)
		return []
	try:
		res = []
		for document in await cursor.to_list(length = 10000):
			try:
				if document.get('_id', None) == None or document.get('name', None) == None:
					continue
				res.append({'id':str(document['_id']), 'name': document['name']})
			except Exception as e:
				logging.error(e)
				continue
		return res
	except Exception as e:
		logging.error(e)
		return []


async def get_groups(category_id):
	try:
		category_id = bson.ObjectId(category_id)
	except Exception as e:
		logging.error(e)
		return []

	try:
		cursor = groups.find({'category': category_id})
	except Exception as e:
		logging.error(e)
		return []

	try:
		res = []
		for document in await cursor.to_list(length = 10000):
			try:
				if document.get('_id', None) == None or document.get('name', None) == None:
					continue
				res.append({'id':str(document['_id']), 'name':document['name']})
			except Exception as e:
				logging.error(e)
				continue
		return res
	except Exception as e:
		logging.error(e)
		return []



async def get_products(category_id, group_id):
	try:
		category_id = bson.ObjectId(category_id)
		group_id = bson.ObjectId(group_id)
	except Exception as e:
		logging.error(e)
		return []

	try:
		cursor = products.find({'category': category_id, 'group':group_id})
	except Exception as e:
		logging.error(e)
		return []

	try:
		res = []
		for document in await cursor.to_list(length = 10000):
			try:
				if document.get('_id', None) == None or document.get('name', None) == None:
					continue
				price = await get_price_in_rub(document['currency'],document['price'])
				name = f"{document['name']} {str(price)} руб."
				res.append({'id':str(document['_id']), 'name':name})
			except Exception as e:
				logging.error(e)
				continue
		return res
	except Exception as e:
		logging.error(e)
		return []

async def get_product_info(product_id):
	try:
		product_id = bson.ObjectId(product_id)
	except Exception as e:
		logging.error(e)
		return None
	try:
		res = await products.find_one({'_id': product_id})
		if res.get('photo', None) is None:
			raise 'No photo'

		if res.get('name', None) is None:
			raise 'No name'


		if res.get('price', None) is None:
			raise 'No price'


		if res.get('currency', None) is None:
			raise 'No currency'

		if res.get('description', None) is None:
			raise 'No description'

		return res
		#return {'photo':f"shop_pictures/{res['photo']}", 'msg':
	except Exception as e:
		logging.error(e)
		return None