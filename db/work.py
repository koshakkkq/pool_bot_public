import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING
import asyncio
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db_work = client.work


async def init_db():
    try:
        users = db_work.users
        await users.drop_indexes()
        index_id = IndexModel([("id", DESCENDING)], unique = True)
        index_phone = IndexModel([("phone", DESCENDING)], unique = True)
        index_lvl = IndexModel([('lvl', DESCENDING)])
        await users.create_indexes([index_id, index_phone, index_lvl])
    except Exception as e:
        print(e)

    try:
        users_description = db_work.users_description
        await users_description.drop_indexes()
        index_id =  IndexModel([("id", DESCENDING)], unique = True)
        index_phone = IndexModel([("phone", DESCENDING)])
        await users_description.create_indexes([index_id, index_phone])
    except Exception as e:
        print(e)

    try:
        objects = db_work.objects
        await objects.drop_indexes()
        index_name = IndexModel([("name", DESCENDING)])
        await objects.create_indexes([index_name])
    except Exception as e:
        print(e)

    try:
        works = db_work.works
        await works.drop_indexes()
        index_id = IndexModel([("timestamp", DESCENDING)])
        await works.create_indexes([index_id])
    except Exception as e:
        print(e)

loop = asyncio.new_event_loop()
loop.run_until_complete(init_db())