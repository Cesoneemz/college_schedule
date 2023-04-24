import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

from sqlalchemy.engine import URL

load_dotenv(find_dotenv())

from handlers import user_messages
from database.database_init import init_database
from database.engine import get_session_maker, create_async_engine


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

DEBUG = os.environ.get('DEBUG')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

dp = Dispatcher()
    
async def main():
    bot = Bot(token=BOT_TOKEN)

    postgresql_url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME')
    )

    engine = create_async_engine(postgresql_url)
    session_maker = get_session_maker(engine)

    await init_database(session_maker=session_maker)

    dp.include_routers(user_messages.router)

    await dp.start_polling(bot, session_maker=session_maker)

if __name__ == "__main__":
    asyncio.run(main())