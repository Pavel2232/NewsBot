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
    refacto_news: bool = False


class PaginationCommentCallbackData(CallbackData, prefix='pagination_comment'):
    id: int
    page: int
    start_index: int = 0
    end_index: int = 1


class BackCallbackData(CallbackData, prefix='back'):
    back: bool = True


class LikeCommentCallbackData(CallbackData, prefix='reactions'):
    id: int
    like: bool = False
    comment: bool = False
    page: int = 1


class WriteCommentCallbackData(CallbackData, prefix='write_comment'):
    write: bool = True


class RefactoringNewsCallbackData(CallbackData, prefix='refactoring_news'):
    id: int
    change_title: bool = False
    change_text: bool = False
    change_all: bool = False
    delete: bool = False
    delete_comment: bool = False
    refacto_news: bool = False
