import aioschedule
import asyncio
import logging
import datetime

import bson

from create import db_project, bot
from shop.currency import get_currency_price

mail = db_project.mail
was_mailed = db_project.was_mailed
subscriptions = db_project.subscriptions

async def mailing():
    try:
        mails = mail.find({})
    except Exception as e:
        logging.error(e)
        return
    for mail_document in await mails.to_list(length = 100000):
        project_id = mail_document.get('project_id', None)
        if project_id == None:
            try:
                await mail.delete_one({'_id':mail_document['_id']})
            except Exception as e:
                logging.error(e)
            continue

        users = subscriptions.find({'project_id':project_id})
        for document in await users.to_list(length = 100000):
            cnt = await was_mailed.count_documents({'user_id':document['user_id'], 'mail_id':mail_document['_id']})
            if cnt == 0:
                try:
                    if mail_document.get('text', None) is not None:
                        await bot.send_message(chat_id=document['user_id'], text=mail_document.get('text', ''))
                    elif mail_document.get('photo_id', None) is not None:
                        await bot.send_photo(chat_id=document['user_id'], photo=mail_document.get('photo_id', None))
                    elif mail_document.get('video_id', None) is not None:
                        await bot.send_video(chat_id=document['user_id'], video=mail_document.get('video_id', None))
                    await was_mailed.insert_one({'user_id':document['user_id'], 'mail_id':mail_document.get('_id'),
                                          'created_at': datetime.datetime.now(datetime.timezone.utc)})
                except Exception as e:
                    logging.error(e)
                    continue


async def scheduler():#todo поменять
    await get_currency_price()
    await mailing()
    aioschedule.every(1).hours.do(mailing)
    aioschedule.every(12).hours.do(get_currency_price)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)
