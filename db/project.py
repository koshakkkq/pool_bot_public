import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING
import asyncio
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db_project = client.project

async def init_db():
    try:
        projects = db_project.projects
        await projects.drop_indexes()
        name = IndexModel([("name", DESCENDING)], unique = True)
        await projects.create_indexes([name])
    except Exception as e:
        print(e)

    try:
        mail = db_project.mail
        await mail.drop_indexes()
        phone = IndexModel([("project_id", DESCENDING)])
        created_at = IndexModel([('created_at', DESCENDING)], expireAfterSeconds = 24*60*60)#24*60*60
        await mail.create_indexes([phone, created_at])
    except Exception as e:
        print(e)


    try:
        was_mailed = db_project.was_mailed
        await was_mailed.drop_indexes()
        phone = IndexModel([("mail_id", DESCENDING)])
        user_id = IndexModel([("user_id", DESCENDING)])
        created_at = IndexModel([('created_at', DESCENDING)], expireAfterSeconds= 2*24*60*60)  #2*24*60*60
        await was_mailed.create_indexes([phone, user_id, created_at])
    except Exception as e:
        print(e)

    try:
        clients = db_project.clients
        await clients.drop_indexes()
        phone = IndexModel([("phone", DESCENDING)])
        id = IndexModel([("id", DESCENDING)])
        await clients.create_indexes([phone, id])
    except Exception as e:
        print(e)

    try:
        subscriptions = db_project.subscriptions
        await subscriptions.drop_indexes()
        phone = IndexModel([("project_id", DESCENDING)])
        id = IndexModel([("user_id", DESCENDING)])
        await subscriptions.create_indexes([phone, id])
    except Exception as e:
        print(e)

    try:
        users = db_project.users
        await users.drop_indexes()
        phone = IndexModel([("phone", DESCENDING)])
        user_id = IndexModel([("user_id", DESCENDING)])
        await users.create_indexes([phone, user_id])
    except Exception as e:
        print(e)





loop = asyncio.new_event_loop()
loop.run_until_complete(init_db())
