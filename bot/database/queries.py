from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, join
from .models import ScheduleEntry, Weekday, SubjectDuration, Subject


async def get_schedule(weekday: str, session_maker: sessionmaker):
    async with session_maker() as session:
        stmt = select(
            Subject.name,
            SubjectDuration.start_time,
            SubjectDuration.end_time,
            SubjectDuration.id
        ).select_from(
            join(ScheduleEntry, Subject)
            .join(SubjectDuration)
            .join(Weekday)
        ).where(
            Weekday.name == weekday
        )
        results = await session.execute(stmt)
        schedule_entries = results.fetchall()

    return schedule_entries
