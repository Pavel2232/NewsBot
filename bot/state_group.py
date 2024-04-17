from aiogram.fsm.state import StatesGroup, State


class UserStart(StatesGroup):
    start = State()
    menu = State()


class WorkWithNews(StatesGroup):
    see_news = State()
    see_comment = State()
    write_comment = State()