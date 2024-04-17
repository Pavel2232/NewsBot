from aiogram.filters.callback_data import CallbackData


class MenuCallbackData(CallbackData, prefix='menu'):
    see_news: bool = False
    create_news: bool = False
    refacto_news: bool = False
