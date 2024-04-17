from aiogram.fsm.state import StatesGroup, State


class UserStart(StatesGroup):
    start = State()
    menu = State()


class WorkWithNews(StatesGroup):
    see_news = State()
    see_comment = State()
    write_comment = State()
    create_news = State()
    write_text_news = State()
    success_create_news = State()
    refacto_news = State()
    change_title = State()
    change_text = State()
    change_all = State()
    delete_news = State()
