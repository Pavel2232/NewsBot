from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from bot.callback_factory import MenuCallbackData, CurrencyNewsCallbackData, LikeCommentCallbackData, \
    WriteCommentCallbackData, BackCallbackData
from bot.service_async import get_all_news, get_all_me_news
from news.models import Like, Comment


def get_start_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='Смотреть Новости',
        callback_data=MenuCallbackData(
            see_news=True
        )
    )

    markup.button(
        text='Создать Новость',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Редактировать Мои Новости',
        callback_data=MenuCallbackData(
            refacto_news=True
        )
    )

    markup.adjust(1)

    return markup.as_markup()


async def get_news_buttons(
        page: int,
        news: list,
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    for novelty in news:
        markup.button(
            text=novelty.title,
            callback_data=CurrencyNewsCallbackData(
                id=novelty.id,
                page=page
            )
        )

    markup.adjust(1)

    return markup.as_markup()


async def comment_like_buttons(id_news: int, page: int = 0) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    like_count: Like = await Like.objects.filter(news_id=id_news, like=True).acount()
    comment_count: Comment = await Comment.objects.filter(news_id=id_news).acount()
    markup.button(
        text=f'{like_count if like_count else ''}❤️',
        callback_data=LikeCommentCallbackData(
            id=id_news,
            like=True,
            page=page
        )
    )

    markup.button(
        text=f'{comment_count if comment_count else ''}💬',
        callback_data=LikeCommentCallbackData(
            id=id_news,
            comment=True,
            page=page
        )
    )

    markup.button(
        text='Назад к новостям',
        callback_data=MenuCallbackData(
            see_news=True,
            page=page
        )
    )

    markup.adjust(2)

    return markup.as_markup()


def add_comment_buttons(id_news: int):
    markup = InlineKeyboardBuilder()

    markup.button(
        text=f'Оставить комментарий',
        callback_data=WriteCommentCallbackData()
    )

    markup.button(
        text='Назад',
        callback_data=CurrencyNewsCallbackData(
            id=id_news
        )
    )

    markup.adjust(1)

    return markup.as_markup()


def get_back_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='Назад',
        callback_data=BackCallbackData()
    )

    markup.adjust(1)

    return markup.as_markup()


def create_more_news_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='Создать ещё новость',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Назад',
        callback_data=BackCallbackData()
    )

    markup.adjust(1)

    return markup.as_markup()


def refactoring_me_news(id_news: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.button(
        text='Изменить заголовок',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Изменить текст',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Изменить всё',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Удалить новость',
        callback_data=MenuCallbackData(
            create_news=True
        )
    )

    markup.button(
        text='Назад',
        callback_data=BackCallbackData()
    )

    markup.adjust(1)

    return markup.as_markup()
