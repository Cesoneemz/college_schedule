from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ScheduleEntry(Base):
    __tablename__ = "schedule_entry"

    id = Column('id', Integer, primary_key=True, unique=True, autoincrement=True)
    subject_code = Column('subject_id', Integer, ForeignKey('subject.subject_code', ondelete='CASCADE'))
    subject = relationship("Subject")
    duration_id = Column('duration_id', Integer, ForeignKey('subject_duration.id'))
    duration = relationship("SubjectDuration")
    weekday_id = Column('weekday_id', Integer, ForeignKey('weekday.id'))
    weekday = relationship("Weekday", back_populates="schedule_entries")

class Subject(Base):
    __tablename__ = "subject"

    subject_code = Column('subject_code', Integer, primary_key=True)
    name = Column('subject_name', String)

class Weekday(Base):
    __tablename__ = "weekday"

    id = Column('id', Integer, primary_key=True)
    name = Column('weekday', String)
    schedule_entries = relationship("ScheduleEntry", back_populates="weekday")

class SubjectDuration(Base):
    __tablename__ = "subject_duration"

    id = Column('id', Integer, primary_key=True)
    start_time = Column('start_time', String)
    end_time = Column('end_time', String)
    schedule_entries = relationship("ScheduleEntry", backref="duration_entry")
