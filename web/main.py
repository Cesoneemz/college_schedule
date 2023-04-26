import os

from flask import Flask, render_template
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, join, text

from dotenv import load_dotenv, find_dotenv

from bot.database.engine import create_async_engine, get_session_maker
from bot.database.models import *

load_dotenv(find_dotenv())


def init_session_maker() -> sessionmaker:
    postgresql_url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME')
    )
    engine = create_async_engine(url=postgresql_url)
    session_maker = get_session_maker(engine=engine)

    return session_maker


async def refill_null(session_maker: sessionmaker):
    stmt = text("UPDATE schedule_entry SET subject_id = 'Пара отсутствует' WHERE subject_id IS NULL")
    async with session_maker() as session:
        await session.execute(stmt)


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.template_folder = 'templates'

session_maker = init_session_maker()


@app.route('/')
async def index():
#    await refill_null(session_maker=session_maker)
    async with session_maker() as session:
        stmt = select(
            Weekday.name,
            Subject.name,
            SubjectDuration.start_time,
            SubjectDuration.end_time,
            SubjectDuration.id,
            ScheduleEntry.auditory_number
        ).select_from(
            join(ScheduleEntry, Subject)
            .join(SubjectDuration)
            .join(Weekday)
        ).order_by(Weekday.id, SubjectDuration.id)
        result = await session.execute(stmt)
        result_with_keys = [dict(zip(result.keys(), row)) for row in result]
        print(result_with_keys)

        schedule = {}
        for row in result_with_keys:
            if row['name'] not in schedule:
                schedule[row['name']] = []
            schedule[row['name']].append(row)

    return render_template('schedule.html', schedule=schedule)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
