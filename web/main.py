import os
import asyncio

from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, join

from pywebio import start_server
from pywebio.output import put_table, put_markdown

from dotenv import load_dotenv, find_dotenv

from bot.database.engine import create_async_engine, get_session_maker
from bot.database.models import ScheduleEntry, Subject, Weekday, SubjectDuration
from bot.database.queries import get_schedule

load_dotenv(find_dotenv())


async def show_all_entries():
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

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for day in days:
        table = [['Номер пары', 'Время', 'Предмет']]
        put_markdown(f"# {day}")
        schedule = await get_schedule(day, session_maker)
        print(schedule)
        for pair in schedule:
            print(pair)
            table.append([pair[3], f"{pair[1]}-{pair[2]}", pair[0]])
        put_table(table)



async def main():
    await show_all_entries()


if __name__ == "__main__":
    start_server(main, port=80)
