import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db_work = client.shop


async def init_db():
	try:
		cart = db_work.cart
		await cart.drop_indexes()
		product_id = IndexModel([("product_id", DESCENDING)])
		user_id = IndexModel([("user_id", DESCENDING)])
		await cart.create_indexes([product_id, user_id])
	except Exception as e:
		print(e)

	try:
		categories = db_work.categories
		await categories.drop_indexes()
		name = IndexModel([("name", DESCENDING)])
		await categories.create_indexes([name])
	except Exception as e:
		print(e)

	try:
		groups = db_work.groups
		await groups.drop_indexes()
		name = IndexModel([("name", DESCENDING)])
		category = IndexModel([("category", DESCENDING)])
		await groups.create_indexes([name, category])
	except Exception as e:
		print(e)

	try:
		products = db_work.products
		await products.drop_indexes()
		group = IndexModel([("group", DESCENDING)])
		category = IndexModel([("category", DESCENDING)])
		await products.create_indexes([group, category])
	except Exception as e:
		print(e)


loop = asyncio.new_event_loop()
loop.run_until_complete(init_db())