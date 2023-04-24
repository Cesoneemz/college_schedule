import datetime

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker

from database.queries import get_schedule

router = Router()

@router.message(Command(commands=["start", "help"]))
async def bot_start_message(message: Message):
    await message.answer("Hello, World!")

@router.message(Command(commands=["schedule"]))
@router.message(lambda message: message.text.lower() in ["сегодня", "завтра"])
async def bot_get_schedule(message: Message, session_maker: sessionmaker):

    if message.text.lower() == "завтра":
        day = datetime.date.today() + datetime.timedelta(days=1)
    else:
        day = datetime.date.today()
    weekday_name = day.strftime("%A")

    schedule_entries = await get_schedule(weekday=weekday_name, session_maker=session_maker)

    message_text = f"Расписание на {'завтра' if message.text.lower() == 'завтра' else 'сегодня'}:\n\n"
    for entry in schedule_entries:
        message_text += f"{entry[1]}-{entry[2]} - {entry[0]}\n"

    await message.answer(message_text)

