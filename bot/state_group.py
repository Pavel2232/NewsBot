from aiogram.fsm.state import StatesGroup, State


class UserStart(StatesGroup):
    start = State()
    menu = State()


class WorkWithNews(StatesGroup):
    see_news = State()