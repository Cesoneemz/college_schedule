from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .models import Subject, Weekday, SubjectDuration

async def create_subject_duration(session_maker: sessionmaker):
    async with session_maker() as session:
        result = await session.execute(text('SELECT EXISTS (SELECT 1 FROM subject_duration)'))
        if not result.scalar():
            start_times = ['8:00', '9:50', '11:50', '13:50', '15:40', '17:25']
            end_times = ['9:40', '11:30', '13:30', '15:30', '17:15', '19:00']

            for start, end in zip(start_times, end_times):
                duration = SubjectDuration(start_time=start, end_time=end)
                session.add(duration)
            
            await session.commit()

async def create_weekdays(session_maker: sessionmaker):
    async with session_maker() as session:
        result = await session.execute(text('SELECT EXISTS (SELECT 1 FROM weekday)'))
        if not result.scalar():
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

            for day in days:
                new_day = Weekday(name=day)
                session.add(new_day)

            await session.commit()

async def init_database(session_maker: sessionmaker):
    await create_weekdays(session_maker=session_maker)
    await create_subject_duration(session_maker=session_maker)