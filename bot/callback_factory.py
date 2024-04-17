from aiogram.filters.callback_data import CallbackData


class MenuCallbackData(CallbackData, prefix='menu'):
    see_news: bool = False
    create_news: bool = False
    refacto_news: bool = False
    page: int = 1


class CurrencyNewsCallbackData(CallbackData, prefix='news'):
    id: int
    page: int = 1


class PaginationCallbackData(CallbackData, prefix='pagination'):
    page: int


class BackCallbackData(CallbackData, prefix='back'):
    back: bool = True


class LikeCommentCallbackData(CallbackData, prefix='reactions'):
    id: int
    like: bool = False
    comment: bool = False
